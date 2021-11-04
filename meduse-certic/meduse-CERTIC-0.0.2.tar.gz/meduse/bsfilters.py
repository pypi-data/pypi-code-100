import bs4

SEARCH_FORM_TEMPLATE = """
    <form action="/_esproxy/" method="get" style="margin-top:150px;" id="search_form">
     <fieldset>
      <legend>Recherche</legend>
         <input type="hidden" name="project_index" value="https-www-unicaen-fr-recherche-mrsh-crdfed-nuremberg">
         <input type="text" name="q" placeholder="Un ou plusieurs mots-clefs">
         <button type="submit">Chercher</button>
      </fieldset>
    </form>
    <ol id="search_results"></ol>
    <script type="text/javascript">
     var searchform = document.getElementById("search_form");
     searchform.addEventListener("submit", (event) => {
      event.preventDefault();
      event.stopPropagation();
      var form_data = new FormData(search_form);
      var request = new XMLHttpRequest();
      request.open("GET", searchform.action + "?q=" + encodeURIComponent(form_data.get("q")) + "&project_index=" + encodeURIComponent(form_data.get("project_index")));
      request.onload = function () {
      if (request.status >= 200 && request.status < 400) {
       var data = JSON.parse(request.responseText);
       var results = document.getElementById("search_results");
       while (results.firstChild) {
        results.removeChild(results.firstChild);
       }
       data.results.hits.forEach(function(element) {
         var li_node = document.createElement("li");
         var a_node = document.createElement("a");
         a_node.href = element._source.path + "?hi=" + encodeURIComponent(data.q);
         var textnode = document.createTextNode(element._source.title);
         a_node.appendChild(textnode);
         li_node.appendChild(a_node);
         results.appendChild(li_node);
       });
       } else {
        alert("Le moteur de recherche ne répond pas.")
       }
      };
      request.send();
     });
    </script>
"""


def remove_logbox(tag_soup: bs4.BeautifulSoup, context: dict = None):
    """
    Boite de login du projet Descartes
    """
    for elem in tag_soup.find_all(id="logbox"):
        elem.decompose()


def remove_noteslink(tag_soup: bs4.BeautifulSoup, context: dict = None):
    """
    Lien d'affichage de l'outil d'annotation
    """
    for elem in tag_soup.find_all(id="notes_link"):
        elem.decompose()


def remove_navigation_select(tag_soup: bs4.BeautifulSoup, context: dict = None):
    for nav_select in tag_soup.find_all("div", {"id": "navigation"}):
        nav_select.decompose()


def fix_empty_ids(tag_soup: bs4.BeautifulSoup, context: dict = None):
    for elem in tag_soup.find_all(
        id=""
    ):  # All elements without ids will be returned as well...
        if elem.has_attr("id"):  # ... so we need an extra check.
            elem.attrs = {
                key: value for key, value in elem.attrs.items() if key not in ["id"]
            }


def fix_empty_form_action(tag_soup: bs4.BeautifulSoup, context: dict = None):
    for elem in tag_soup.find_all("form", {"action": ""}):
        elem.attrs = {
            key: value for key, value in elem.attrs.items() if key not in ["action"]
        }


def replace_search_form_action(tag_soup: bs4.BeautifulSoup, context: dict = None):
    """
    Remplace le formulaire de recherche d'origine.
    """
    for elem in tag_soup.find_all(id="querymodule"):
        elem["action"] = "/_esproxy/"
        new_soup = bs4.BeautifulSoup(
            '<input type="hidden" name="project_identifier" value="{}">'.format(
                context["project_identifier"]
            ),
            features="lxml",
        )
        elem.append(new_soup.input)
