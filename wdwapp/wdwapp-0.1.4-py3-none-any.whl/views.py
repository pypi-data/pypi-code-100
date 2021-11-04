""" Main programm 

Show wheater data and mamange configuration

To do
- Add message to send with alarm
- Add authentication to allow some users to change values and/or
  configuration data.
- Added auth.secret in ini files. Please merge your ini files with them on
  http://static.frkb.fr/wdwapp
- Add .ini parameter to define period of detail view.
"""
import colander
import deform.widget
# ~ import pdb
# ~ pdb.set_trace()

from wdwapp import __version__, __year__

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
)

from .models import (
    DBSession,
    Location,
    Sensor,
    WeatherData,
)

from sqlalchemy import desc, func

from datetime import datetime, timedelta

class WdPage(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )

# ~ class LocFile(object):
    # ~ "Class to store location data in mémory"
    # ~ def __init__(self):
        # ~ self.data = []
    # ~ def write(self, stuff):
        # ~ self.data.append(stuff)
    # ~ def read(self):
        # ~ return self.data


class WeatherViews(object):
    def __init__(self, request):
        self.request = request
        self.mode = ''
        self.version = __version__
        self.year = __year__
        self.stg = self.request.registry.settings
        self.t_unit = self.stg['wd.t_unit'].upper()
        minutes = int(self.stg['wd.max_data_age'])
        self.max_age = timedelta(minutes=minutes)

    def refresh_locations(self):

        "Load location data"

        # Load session data
        session = self.request.session

        # Retrieve and read last data for active locations
        locations = []
        for loc in DBSession.query(Location).filter_by(active = True).order_by('rank'):
            
            # Read location data
            lt = DBSession.query(func.max(WeatherData.timestp)).filter_by(lid = loc.id)[0][0]
            wdt = DBSession.query(WeatherData).filter_by(lid = loc.id, timestp = lt)[0]
            sns = DBSession.query(Sensor).filter_by(id = loc.sid)[0]
            
            # Decode battery level
            if not sns.bat_low:
                batlevel = "OK"
            else:
                batlevel = "vide"
            
            # Verify if data is up to date
            if sns.last_seen < datetime.now() - self.max_age:
                uptodate = 'KO'
            else:
                uptodate = 'OK'
            
            # Get possible nul values and arrange them
            lsee = 'Jammais' if sns.last_seen == None else sns.last_seen.strftime('%d %b %Y à %H:%M')
            lchg = 'Jamais' if sns.last_bat_chg == None else sns.last_bat_chg.strftime('%d %b %Y à %H:%M')
            nchg = '0' if sns.nbr_bat_chg == None else str(sns.nbr_bat_chg)
            
            
            # Fill template data
            locations.append({'id': loc.id,
                'name': loc.name,
                'temperature': str(round(wdt.temperature, 1)),
                'humidity': wdt.humidity,
                'tunit': '°' + self.t_unit,
                'bat_level': batlevel,
                'uptodate': uptodate,
                'last_seen': lsee,
                'last_chg': lchg,
                'numb_chg': nchg,
                'sns_id': sns.id })
        session['locations'] = locations
    
    @property
    def wd_form(self):
        schema = WdPage()
        btns=['submit',]
        if self.mode == 'e':
            btns.append('delete')
        return deform.Form(schema, buttons=btns)


    @property
    def reqts(self):
        return self.wd_form.get_widget_resources()


    @view_config(route_name='overview', renderer='templates/overview.pt')
    def overview(self):

        """Main view with an overview of locations
        """

        # Load session data
        session = self.request.session

        # Get last reading time
        lt = DBSession.query(func.max(WeatherData.timestp))
        ltime = lt[0][0].strftime('%d %b à %H:%M')
        
        self.refresh_locations()
        locations = session['locations']

        return dict(ltime=ltime, datas=locations)

    
    @view_config(route_name='detail', renderer='templates/detail.pt')
    def detail(self):

        """Detail of a location.
            Display the list of last 24h.
        """
        
        # Load session data
        session = self.request.session

        # Get actual location id
        lid = int(self.request.matchdict['lid'])
        
        # Populate navigation data
        nav = {}
        if "locations" not in session:
            self.refresh_locations()
        locations = session['locations']
        nbr = len(locations)
        for i in range(nbr):
            if locations[i]['id'] == lid:
                act = i
                break
        prev = act - 1
        if prev < 0:
            prev = nbr -1
        next = act + 1
        if next > nbr - 1:
            next = 0
        nav['prev_id'] = locations[prev]['id']
        nav['prev_name'] = locations[prev]['name']
        nav['next_id'] = locations[next]['id']
        nav['next_name'] = locations[next]['name']
        
        # Get actual location data
        lname = DBSession.query(Location.name, Location.sid).filter_by(id = lid)[0][0]
        datas = DBSession.query(WeatherData).\
                filter_by(lid = lid).\
                filter(func.MINUTE(WeatherData.timestp) == 0).\
                order_by(desc('timestp')).limit(96).all()
        return dict(lname = lname, datas = datas,
            tunit = '°' + self.t_unit, nav = nav)


    @view_config(route_name='chgbat')
    def chgbat(self):

        "Update battery data"
        
        # Load session data
        session = self.request.session

        # Get actual location id
        sid = int(self.request.matchdict['sid'])
        
        # Get sensor data
        sns = DBSession.query(Sensor).filter_by(id = sid).one()
        
        # Update battery data
        sns.last_bat_chg = datetime.now()
        if sns.nbr_bat_chg == None:
            sns.nbr_bat_chg = 1
        else:
            sns.nbr_bat_chg += 1
        
        # Refresh detail view
        return HTTPFound(self.request.route_url('overview'))


    # ~ @view_config(route_name='wikipage_add',
                 # ~ renderer='wikipage_addedit.pt')
    # ~ def wikipage_add(self):
        # ~ self.mode = 'a'
        # ~ form = self.wd_form.render()

        # ~ if 'submit' in self.request.params:
            # ~ controls = self.request.POST.items()
            # ~ try:
                # ~ appstruct = self.wd_form.validate(controls)
            # ~ except deform.ValidationFailure as e:
                # ~ # Form is NOT valid
                # ~ return dict(form=e.render())

            # ~ # Form is valid, Add a new page to the database
            # ~ new_title = appstruct['title']
            # ~ new_body = appstruct['body']
            # ~ DBSession.add(Page(title=new_title, body=new_body))

            # ~ # Get the new ID and redirect
            # ~ page = DBSession.query(Page).filter_by(title=new_title).one()
            # ~ new_uid = page.uid

            # ~ # Now visit new page
            # ~ url = self.request.route_url('wikipage_view', uid=new_uid)
            # ~ return HTTPFound(url)

        # ~ return dict(form=form)

    # ~ @view_config(route_name='wikipage_edit',
                 # ~ renderer='wikipage_addedit.pt')
    # ~ def wikipage_edit(self):
        # ~ uid = self.request.matchdict['uid']
        # ~ page = DBSession.query(Page).filter_by(uid=uid).one()

        # ~ self.mode = 'e'
        # ~ wd_form = self.wd_form

        # ~ if 'submit' in self.request.params:
            # ~ controls = self.request.POST.items()
            # ~ try:
                # ~ appstruct = wd_form.validate(controls)
            # ~ except deform.ValidationFailure as e:
                # ~ return dict(page=page, form=e.render())

            # ~ # Change the content and redirect to the view
            # ~ page.title = appstruct['title']
            # ~ page.body  = appstruct['body']

            # ~ url = self.request.route_url('wikipage_view', uid=uid)
            # ~ return HTTPFound(url)
        
        # ~ if 'delete' in self.request.params:
            # ~ session = self.request.session
            # ~ session['msg'] = 'Page "' + page.title + '" deleted.'
            # ~ DBSession.delete(page)

            # ~ url = self.request.route_url('wiki_view')
            # ~ return HTTPFound(url)

        # ~ form = wd_form.render(dict(
            # ~ uid=page.uid, title=page.title, body=page.body)
        # ~ )

        # ~ return dict(page=page, form=form)

    # ~ @view_config(route_name='home')
    # ~ def home(self):
        # ~ first = self.request.matchdict['first']
        # ~ last = self.request.matchdict['last']
        # ~ return {
            # ~ 'name': 'Home View',
            # ~ 'first': first,
            # ~ 'last': last
        # ~ }
