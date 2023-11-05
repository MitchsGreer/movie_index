"""Webpage for the main page, written as a string to make my life easier."""


MOVIE_TITLE_INPUT = "movie_name"
MOVIE_SOURCES_OUTPUT = "movie_sources"
MOVIE_SOURCE_SELECTION_INPUT = "movie_source_selection"
SUBMIT_BUTTON_INPUT = "submit"
ADD_MOVIE_SUBMIT_VALUE = "Add Movie"
GEN_RAND_SUBMIT_VALUE = "Generate Random Movie"

INDEX_PAGE = """
<!doctype html>
<center>

{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class=flashes>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

 <!-- Tab links -->
<div class="tab">
  <button class="tablinks" onclick="openCity(event, 'add_movie')">Add Movie</button>
  <button class="tablinks" onclick="openCity(event, 'gen_rand_movie')">Generate Random Movie</button>
</div>

<!-- Tab content -->
<div id="add_movie" class="tabcontent">
  <h3>Add Movie</h3>
  <form action="/" method="POST">
        <label for="movie_name">Movie Title:</label>
        <input type="text" id="movie_name" name="movie_name" required=true />
        <br>
        <br>
        <label for="movie_source_selection">Select Movie Source(s):</label>
        <br>
        <select name=movie_source_selection id=movie_source_selection multiple=true required=true size=3>
        {% for source in movie_sources %}
            <option value="{{ source }}">{{ source }}</option>
        {% endfor %}
        </select>
        <br>
        <br>
        <input type="submit" name="submit" id="submit" value="Add Movie" />
    </form>
</div>

<div id="gen_rand_movie" class="tabcontent" style="display: none;">
  <h3>Generate Random Movie</h3>
  <form action="/" method="POST">
        <input type="submit" name="submit" id="submit" value="Generate Random Movie" />
    </form>
</div>
</center>
{% block body %}{% endblock %}

<script>
function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
</script>
"""
