""" In this file there are some functions to manage the GUI and the pyQT import """
try:
    QT = 4
    import PyQt4.QtGui as QtG
    import PyQt4.QtCore as QtCore
    from PyQt4.QtGui import QFontMetrics,QFont
    import matplotlib.backends.backend_qt4agg as plt_qtbackend
except ImportError:
    QT = 5
    import PyQt5.QtWidgets as QtG
    from PyQt5.QtGui import QFontMetrics,QFont
    import PyQt5.QtCore as QtCore
    import matplotlib.backends.backend_qt5agg as plt_qtbackend

import matplotlib.pyplot as plt
from cryoloBM import constants,helper_image,helper
from imageio import mimsave
from os import path
from typing import List
import numpy as np

from cryoloBM import boxmanager_view,boxmanager_controller    # for type hinting purpose
from skimage.transform import resize

def apply_to_all_the_tomo_question(view:boxmanager_view, name_param:str)->int:
    msg = f"Do you want to change '{ name_param} ' to all tomographies"
    return QtG.QMessageBox.question(view, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No)


def err_message(view:boxmanager_view, msg:str)->None:
    """
    shows the pop up window with the 'msg' error message
    :param view: Boxmanager_view obj
    :param msg: message visualized on the pop up window
    """
    errmsg = QtG.QErrorMessage(view)
    errmsg.showMessage(msg)

def qtmessage(view:boxmanager_view, msg:str, has_cancel:bool)->int:
    """
    shows the pop up question message and returns the inserted answer
    :param view: Boxmanager_view obj
    :param msg: message visualized on the pop up window
    :param has_cancel: If True it has 'QtG.QMessageBox.Cancel' instead of 'QtG.QMessageBox.No'
    :return 'QtG.QMessageBox.question'
    """
    second_choice = QtG.QMessageBox.Cancel if has_cancel else QtG.QMessageBox.No
    return QtG.QMessageBox.question(view, "Message", msg, QtG.QMessageBox.Yes, second_choice)

def qt_esixting_folder(view:boxmanager_view, msg:str)->str:
    """
    shows the pop up question message and returns the inserted answer
    :param view: Boxmanager_view obj
    :param msg: message visualized on the pop up window
    :return the path as string
    """
    return str( QtG.QFileDialog.getExistingDirectory(view, msg) )

def get_selected_folder(view:boxmanager_view, unsaved_changes:bool)->str:
    """
    Set image_folder_path. It is selected by the user via GUI
    :param view: Boxmanager_view obj
    :param unsaved_changes:
    :return The selected folder
    """
    selected_folder = qt_esixting_folder(view, msg = "Select Image Directory")

    if selected_folder == "" or (
            unsaved_changes and qtmessage(view, msg="All loaded boxes are discarded. Are you sure?",
                                                has_cancel=True) == QtG.QMessageBox.Cancel):
        return ""
    return  selected_folder

def get_selected_file(view:boxmanager_view, unsaved_changes:bool)->str:
    """
    Set current_image_path. It is selected by the user via GUI
    :param view: Boxmanager_view obj
    :param unsaved_changes:
    :return The selected file
    """
    selected_image = QtG.QFileDialog.getOpenFileName(view, "Select 3D Image File")[0]

    if selected_image == "" or (
            unsaved_changes and qtmessage(view, msg="All loaded boxes are discarded. Are you sure?",
                                                has_cancel=True) == QtG.QMessageBox.Cancel):
        return ""
    return selected_image

def add_item_combobox(name:str, obj:QtG.QComboBox)->None:
    """
    Adds the 'name' item of the 'obj' combobox if it is not present
    :param name: string name of the item
    :param obj: QtG.QComboBox obj
    """
    pos = get_pos_item_combobox(name=name, obj=obj)
    if pos == -1:
        obj.addItems([name])


def remove_item_combobox(name:str, obj:QtG.QComboBox)->None:
    """
    Removes the 'name' item of the 'obj' combobox if it is present
    :param name: string name of the item
    :param obj: QtG.QComboBox obj
    """
    pos = get_pos_item_combobox(name=name, obj=obj)
    if pos > -1:
        obj.removeItem(pos)

def get_pos_item_combobox(name:str, obj:QtG.QComboBox)->int:
    """
    Returns the position of the 'name' item of the 'obj' combobox. -1 f it is not present
    :param name: string name of the item
    :param obj: QtG.QComboBox obj
    :return: position in list
    """
    #AllItems = [ for i in range(obj.count())]
    for i in range(obj.count()):
        if name == obj.itemText(i):
            return i
    return -1

def delete_all_items_combobox(obj:QtG.QComboBox)->None:
    """
    Deletes all the items in the given combobox obj
    :param obj: QtG.QComboBox obj
    """
    for i in range(obj.count()-1,-1,-1):
        remove_item_combobox(obj.itemText(i),obj)

def fill_root_childs(root:QtG.QTreeWidgetItem, tot_slices:int, is_folder:bool =False, root_child_index:int =None)->None:
    """
    Creates all the checkboxes of a given tomogram in the GUI
    :param root: The 'QTreeWidgetItem' obj represent the item list (namely the filenames)
    :param tot_slices:  number of slices present in the tomogram
    :param is_folder: True if we loaded a folder of tomo
    :param root_child_index: index of child in root. It is the item, which represent a tomogram in a folder
    """
    for i in range(tot_slices):
        QtCore.QCoreApplication.instance().processEvents()
        c = QtG.QTreeWidgetItem([str(i)])
        c.setCheckState(0, QtCore.Qt.Unchecked)
        if is_folder:
            root.child(root_child_index).addChild(c)
        else:
            root.addChild(c)

def uncheck_all_slides(view:boxmanager_view, type_case:int)->None:
    """
    Uncheck all the checked checkboxes
    :param view: Boxmanager_view obj
    :param type_case: constants.Type_case. value
    """
    # uncheck all the checked slices (tomo cases) or images (SPA cases)
    for root_index in range(view.tree.invisibleRootItem().childCount()):
        root_element = view.tree.invisibleRootItem().child(root_index)  # can be tomogram or a folder
        root_element.setCheckState(0, QtCore.Qt.Unchecked)
        for child_index in range(root_element.childCount()):
            root_element.child(child_index).setCheckState(0, QtCore.Qt.Unchecked)
            if type_case == constants.Type_case.TOMO_FOLDER.value:
                for child_child_index in range(root_element.child(child_index).childCount()):
                    root_element.child(child_index).child(child_child_index).setCheckState(0, QtCore.Qt.Unchecked)

def event_checkbox_changed(item:QtG.QTreeWidgetItem, column:int)->None:
    """
    Clicking on a node of a checkbox tree set as checked all its children recursively
    It is called directly by box_manager_view. It fills the input params in automatic
    """
    if column == 0:
        if item.childCount()>0:
            for child_index in range(item.childCount()):
                item.child(child_index).setCheckState(0,item.checkState(0))

def tracing_tab_blurring(view:boxmanager_view, is_enable:bool, has_filament:bool)->None:
    """
    After loading from file we have to unblur some options in tracing  tabs
    :param view: Boxmanager_view obj
    :param is_enable: If True enable the options
    :param has_filament: If True we work with filament
    """

    view.search_range_label.setEnabled(is_enable)
    view.search_range_line.setEnabled(is_enable)
    view.search_range_slider.setEnabled(is_enable)
    view.memory_line.setEnabled(is_enable)
    view.memory_label.setEnabled(is_enable)
    view.memory_slider.setEnabled(is_enable)
    view.min_length_label.setEnabled(is_enable)
    view.min_length_line.setEnabled(is_enable)
    view.min_length_slider.setEnabled(is_enable)
    view.preview_label.setEnabled(is_enable)
    view.preview_checkbox.setEnabled(is_enable)
    view.button_trace.setEnabled(is_enable)

    # usable only in filament case
    is_enable = is_enable and has_filament  # True only if both are True

    view.min_edge_weight_slider.setEnabled(is_enable)
    view.min_edge_weight_line.setEnabled(is_enable)
    view.min_edge_weight_label.setEnabled(is_enable)
    view.win_size_line.setEnabled(is_enable)
    view.win_size_slider.setEnabled(is_enable)
    view.win_size_label.setEnabled(is_enable)

def thresholding_tab_blurring_(view:boxmanager_view, is_enable:bool, kind_of_cbox:bool, has_filament:bool, type_case:int)->None:
    """
    After loading from file we have to unblur some options in thresholding tabs
    :param view: Boxmanager_view obj
    :param is_enable: If True enable SOME options. If False disable ALL the options
    :param kind_of_cbox: True if model.is_cbox or model.is_cbox_untracved is True
    :param has_filament: If True we work with filament
    :param type_case: constants.Type_case. value
    """
    if kind_of_cbox or not is_enable:
        view.conf_thresh_line.setEnabled(is_enable)
        view.conf_thresh_slide.setEnabled(is_enable)
        view.conf_thresh_label.setEnabled(is_enable)
        view.use_estimated_size_label.setEnabled(is_enable)
        view.use_estimated_size_checkbox.setEnabled(is_enable)
        view.show_confidence_histogram_action.setEnabled(is_enable)
        view.show_size_distribution_action.setEnabled(is_enable)
        if not has_filament or not is_enable:
            view.upper_size_thresh_label.setEnabled(is_enable)
            view.upper_size_thresh_slide.setEnabled(is_enable)
            view.upper_size_thresh_line.setEnabled(is_enable)
            view.lower_size_thresh_label.setEnabled(is_enable)
            view.lower_size_thresh_slide.setEnabled(is_enable)
            view.lower_size_thresh_line.setEnabled(is_enable)
        if type_case in [constants.Type_case.TOMO.value, constants.Type_case.TOMO_FOLDER.value] or not is_enable:
            view.num_boxes_thresh_slide.setEnabled(is_enable)
            view.num_boxes_thresh_line.setEnabled(is_enable)
            view.num_boxes_thres_label.setEnabled(is_enable)

def update_low_up_thresh(view:boxmanager_view,max_size:int,min_size:int)->None:
    """
    After loading from file we have to update upper and lower threshold values
    :param view: Boxmanager_view obj
    :param max_size: max size value
    :param min_size: min size value
    """
    view.is_updating_params = True
    view.upper_size_thresh_slide.setMaximum(max_size)
    view.upper_size_thresh_slide.setMinimum(min_size)
    view.upper_size_thresh_slide.setValue(max_size)
    view.upper_size_thresh_line.setText("" + str(max_size))
    view.lower_size_thresh_slide.setMaximum(max_size)
    view.lower_size_thresh_slide.setMinimum(min_size)
    view.lower_size_thresh_slide.setValue(min_size)
    view.lower_size_thresh_line.setText("" + str(min_size))
    view.is_updating_params = False

def set_checkstate_tree_leafs( item:QtG.QTreeWidgetItem, entries:List[str], state:QtCore.Qt.CheckState)->None:
    """
    Check or uncheck the checkboxes in the tree
    :param item: controller.view.tree.invisibleRootItem()
    :param entries: list of entries as strings (e.g.: list of slices)
    :param state: helper_GUI.QtCore.Qt.Checked or helper_GUI.QtCore.Qt.Unchecked
    """
    child_count = item.childCount()
    child_child_counter = item.child(0).childCount()
    if child_child_counter>0:
        for child_id in range(child_count):
            set_checkstate_tree_leafs(item.child(child_id),entries,state)
    else:
        for child_id in range(child_count):
            parent_identifier = path.splitext(item.text(0))[0]
            dict_identifier = path.splitext(item.child(child_id).text(0))[0]
            if len(entries) == 0:
                return
            if type(entries[0]) is tuple:
                parent_entries = [entry[0] for entry in entries]
                child_entries = [entry[1] for entry in entries]
                for k in range(len(entries)):
                    if parent_identifier == parent_entries[k] and dict_identifier == child_entries[k]:
                        item.child(child_id).setCheckState(0,state)

            else:
                if dict_identifier in entries:
                    item.child(child_id).setCheckState(0,state)

def display_default_params(view:boxmanager_view)->None:
    """
    After resetting (file->reset or loading new images) i have to set the default vars as at the start
    :param view: boxmanager_view obj
    """
    view.is_updating_params = True
    view.upper_size_thresh_line.setText(str(constants.Default_settings_value.DEFAULT_UPPER_SIZE_THRESH.value))
    view.lower_size_thresh_line.setText(str(constants.Default_settings_value.DEFAULT_LOWER_SIZE_THRESH.value))
    view.conf_thresh_line.setText(str(constants.Default_settings_value.DEFAULT_CURRENT_CONF_THRESH.value))
    view.num_boxes_thresh_line.setText(str(constants.Default_settings_value.DEFAULT_CURRENT_NUM_BOXES_THRESH.value))
    view.memory_line.setText(str(constants.Default_settings_value.DEFAULT_MEMORY.value))
    view.search_range_line.setText(str(constants.Default_settings_value.DEFAULT_SEARCH_RANGE.value))

    view.min_length_line.setText(str(constants.Default_settings_value.DEFAULT_MIN_LENGTH.value))
    view.win_size_line.setText(str(constants.Default_settings_value.DEFAULT_BOX_SIZE.value))
    view.min_edge_weight_line.setText(str(constants.Default_settings_value.DEFAULT_MIN_EDGE_WEIGHT.value))
    view.is_updating_params = False

def set_enable_save_gif(view,is_enable: bool) -> None:
        """
        It makes the 'save gif' option enable or not
        :param view: boxmanager_view obj
        :param is_enable: True makes enable this widget
        """
        view.save_data_gif.setEnabled(is_enable)

def set_visibility_box_distance(view,is_visible: bool) -> None:
        """
        It makes the 'box distance' buttons and line of the 'visualization' tab visible or not
        :param view: boxmanager_view obj
        :param is_visible: True makes visible these widgets
        """
        view.button_set_box_distance_filament.setVisible(is_visible)
        view.box_distance_filament_label.setVisible(is_visible)
        view.box_distance_filament_line.setVisible(is_visible)

def set_visualization_combobox(view, is_picking_particles: bool) -> None:
    """
    It fills the 'visualization' combobox of the 'visualization' tab in function of the picking combobox value
    :param view: boxmanager_view obj
    :param is_picking_particles: True if the picking combobox is set to 'Particles'
    """
    delete_all_items_combobox(obj=view.visualization_combobox)
    values = [constants.Visualization_cb.RECT.value,
              constants.Visualization_cb.CIRCLE.value] if is_picking_particles \
        else [constants.Visualization_cb.RECT_FILAMENT_START_END.value,
              constants.Visualization_cb.RECT_FILAMENT_SEGMENTED.value,
              constants.Visualization_cb.CIRCLE_SEGMENTED.value]
    for item_name in values:
        add_item_combobox(name=item_name, obj=view.visualization_combobox)

def set_picking_combobox(view, is_enabled: bool) -> None:
    """
    It fills the picking combobox of the main window
    :param view: boxmanager_view obj
    :param is_enabled: False it is blurred
    """
    values = [constants.Picking_cb.PARTICLE.value, constants.Picking_cb.FILAMENT.value]

    delete_all_items_combobox(obj=view.picking_filament_combox)
    for item_name in values:
        add_item_combobox(name=item_name, obj=view.picking_filament_combox)

    view.picking_filament_combox.setEnabled(is_enabled)


class SaveGifWindow(QtG.QMainWindow):
    def __init__(self, controller:boxmanager_controller,fframe:int)->None:
        super().__init__(None)

        self.errmsg = QtG.QErrorMessage(self)

        self.controller = controller

        self.last_valid_index = controller.model.tot_frames[controller.get_current_filename(with_extension=False) ] - 1
        self.first_index = controller.model.index_tomo
        self.last_index = self.last_valid_index
        self.freq_frame = fframe
        self.output_file = "output.gif"
        self.downsize_factor = 1

        # SETUP QT
        self.font = controller.view.font
        self.setWindowTitle("BoxManager Save on gif")

        central_widget = QtG.QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QtG.QGridLayout(central_widget)

        line_counter = 1
        self.first_index_label = QtG.QLabel("First slice: ")
        self.first_index_line = QtG.QLineEdit(str(self.first_index))
        self.first_index_line.returnPressed.connect(self.first_index_changed)

        self.layout.addWidget(self.first_index_label, line_counter, 0)
        self.layout.addWidget(self.first_index_line, line_counter, 1)
        line_counter +=1

        self.last_index_line = QtG.QLineEdit(str(self.last_index))
        self.last_index_label = QtG.QLabel("Last slice: ")
        self.last_index_line.returnPressed.connect(self.last_index_changed)

        self.layout.addWidget(self.last_index_label, line_counter, 0)
        self.layout.addWidget(self.last_index_line, line_counter, 1)
        line_counter +=1

        self.downsize_factor_line = QtG.QLineEdit(str(self.downsize_factor))
        self.downsize_factor_label = QtG.QLabel("Resize (downsize factor): ")
        self.downsize_factor_line.returnPressed.connect(self.downsize_factor_changed)

        self.layout.addWidget(self.downsize_factor_label, line_counter, 0)
        self.layout.addWidget(self.downsize_factor_line, line_counter, 1)
        line_counter +=1

        self.frequency_line = QtG.QLineEdit(str(self.freq_frame))
        self.frequency_label = QtG.QLabel("Frequency [frame/sec]: ")
        self.frequency_line.returnPressed.connect(self.frequency_changed)

        self.layout.addWidget(self.frequency_label, line_counter, 0)
        self.layout.addWidget(self.frequency_line, line_counter, 1)
        line_counter +=1

        self.savename_line = QtG.QLineEdit(self.output_file)
        self.savename_label = QtG.QLabel("Output file: ")
        self.savename_line.returnPressed.connect(self.savename_changed)

        self.layout.addWidget(self.savename_label, line_counter, 0)
        self.layout.addWidget(self.savename_line, line_counter, 1)
        line_counter +=1

        self.button_save = QtG.QPushButton("Save")
        self.button_save.clicked.connect(self.save)

        self.layout.addWidget(self.button_save, line_counter, 0)
        line_counter +=1

    @staticmethod
    def line_setText(line:QtG.QLineEdit,value:str )->None:
        """
        Set the value into the line (e.g: boxsize line)
        """
        line.setText(value)

    def savename_changed(self)->bool:
        self.output_file=self.savename_line.text()
        return True

    def check_valid_index(self,line:QtG.QLineEdit, old_value:int, index:int)->bool:
        """
        Check if the index is a valid one
        :param old_value: last valid value
        :param line: QLineEdit obj
        :param index: index value
        """
        valid = 0<=index<=self.last_valid_index
        if not valid:
            self.line_setText(line=line, value=str(old_value))
            self.errmsg.showMessage(f"Value out of range. The indexes have to be into [0,{self.last_valid_index}]")
        return valid


    def first_index_changed(self)->bool:
        old_value = self.first_index
        try:
            value = int(float(self.first_index_line.text()))
            if not self.check_valid_index(line=self.first_index_line,old_value=old_value, index = value):
                return False
            self.first_index = value
        except ValueError:
            self.line_setText(line=self.first_index_line, value=str(old_value))
            self.errmsg.showMessage("Invalid value. The first index has to be a positive number")
            return False
        return True

    def last_index_changed(self)->bool:
        old_value = self.last_index
        try:
            value = int(float(self.last_index_line.text()))
            if not self.check_valid_index(line=self.last_index_line,old_value=old_value, index = value):
                return False
            self.last_index = value
        except ValueError:
            self.line_setText(line=self.last_index_line, value=str(old_value))
            self.errmsg.showMessage("Invalid value. The last index has to be a positive number")
            return False
        return True

    def downsize_factor_changed(self)->bool:
        old_value = self.downsize_factor
        try:
            value = float(self.downsize_factor_line.text())
            if value<0:
                self.errmsg.showMessage("Invalid value. The downsize factor has to be a positive number")
                return False
            self.downsize_factor = value
        except ValueError:
            self.line_setText(line=self.downsize_factor_line, value=str(old_value))
            self.errmsg.showMessage("Invalid value. The downsize factor has to be a positive number")
            return False
        return True

    def frequency_changed(self)->bool:
        old_value = self.freq_frame
        try:
            value = int(float(self.frequency_line.text()))
            if value<1:
                self.errmsg.showMessage("Invalid value. The frequency has to be a positive number")
                return False
            self.freq_frame = value
        except ValueError:
            self.line_setText(line=self.frequency_line, value=str(old_value))
            self.errmsg.showMessage("Invalid value. The frequency has to be a positive number")
            return False
        return True

    def draw_all_patches(self,ax) -> None:
        """
        Draws all the patches present in model.rectangle var
        Since model.rectangle is a reference to a list of particle_dictionary dict it has to fill in the appropriate way
        :param ax: ax
        """
        current_conf_thresh, upper_size_thresh, lower_size_thresh, current_num_boxes_thresh = self.controller.model.get_threshold_params(filename=None)
        has_filament = self.controller.model.picking_combobox_value == constants.Picking_cb.FILAMENT.value
        is_circle = self.controller.model.visualization in [constants.Visualization_cb.CIRCLE.value,
                                                       constants.Visualization_cb.CIRCLE_SEGMENTED.value]

        # remove the instances for avoiding "RuntimeError: Can not put single artist in more than one figure"
        for box in self.controller.model.rectangles:
            box.remove_instances()

        visible_sketches = [box.getSketch(circle=is_circle) for box in self.controller.model.rectangles if
                            helper.check_if_should_be_visible(box=box, current_conf_thresh=current_conf_thresh,
                                                              upper_size_thresh=upper_size_thresh,
                                                              lower_size_thresh=lower_size_thresh,
                                                              num_boxes_thresh=current_num_boxes_thresh,
                                                              is_filament=has_filament)]

        for sketch in visible_sketches:
            if not sketch.get_visible():
                sketch.set_visible(True)

            ax.add_patch(sketch)
            ax.draw_artist(sketch)

    def add_plot(self,)->List[np.ndarray]:
        """
        Add boxes to np images
        """
        images = self.controller.model.current_tomoimage_mmap[self.first_index: self.last_index, :, :]
        imgs=list()
        figsize=plt.figaspect(images[0])
        for i,im in enumerate(images):
            fig, ax = plt.subplots(figsize=figsize)
            fig.subplots_adjust(0, 0, 1, 1)

            ax.imshow(im, origin="lower", cmap="gray", interpolation="Hanning", vmin=-5, vmax=5)

            helper_image.set_and_update_boxdictionary_image_changed(controller=self.controller,index_tomo=self.first_index + i)

            fig.canvas.draw()
            self.draw_all_patches(ax=ax)

            im = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            w, h = fig.canvas.get_width_height()

            im=im.reshape((int(h), int(w), -1))
            if self.downsize_factor != 1:
                im = resize(im, (im.shape[0] //self.downsize_factor, im.shape[1]//self.downsize_factor ), anti_aliasing=True)
            imgs.append(im)
            del fig,ax
        # restore the 'self.controller.model.rectangles' for the current_image (the one is shown)
        helper_image.set_and_update_boxdictionary_image_changed(controller=self.controller,index_tomo=self.controller.model.index_tomo)
        return imgs

    def blur_it(self)->None:
        """
        When it is saving on file, all the option will be blurred
        """
        self.button_save.setEnabled(False)
        self.first_index_label.setEnabled(False)
        self.first_index_line.setEnabled(False)
        self.last_index_line.setEnabled(False)
        self.last_index_label.setEnabled(False)
        self.frequency_line.setEnabled(False)
        self.frequency_label.setEnabled(False)
        self.downsize_factor_line.setEnabled(False)
        self.downsize_factor_label.setEnabled(False)
        self.savename_line.setEnabled(False)
        self.savename_label.setEnabled(False)

    def save(self)->None:
        if self.last_index<self.first_index:
            self.errmsg.showMessage(f"Invalid index values. The last index ({self.last_index}) is lower the first index ({self.first_index})")
            return
        if not all([self.frequency_changed(), self.first_index_changed(), self.last_index_changed(), self.savename_changed(), self.downsize_factor_changed()]):
            return
        selected_folder = qt_esixting_folder(self, msg="Select Directory")
        self.blur_it()
        mimsave(uri=path.join(selected_folder,self.output_file),ims=self.add_plot(),format='GIF',fps=self.freq_frame)
        self.close()
