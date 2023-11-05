"""Webpage for the main page, written as a string to make my life easier."""


MOVIE_TITLE_INPUT = "movie_name"
MOVIE_SOURCE_SELECTION_INPUT = "movie_source_selection"
SUBMIT_BUTTON_INPUT = "submit"

WEBPAGE = """
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

"""
