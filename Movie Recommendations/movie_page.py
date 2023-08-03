def create_page_html(movie_name, movie_data, index):
    page_url = "movie_page.html"

    with open("templates/" + page_url, "w") as page:
        html_code = f'''
        <!DOCTYPE html>
<html>
    <head>
        <title>{movie_data[index]["Title"]}</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="../static/styles/movie_style.css">
    </head>
    <body>
        <h1>{movie_data[index]["Title"]}</h1>
        <img src="https://image.tmdb.org/t/p/w500{movie_data[index]["Movie Poster"]}" alt="{movie_data[index]["Title"]} Poster">
        <p>Rating: {movie_data[index]["Rating"]}</p>
        <p>Genres: {movie_data[index]["Genres"]}</p>
        <p>Release date: {movie_data[index]["Release date"]}</p>
        <p>Overview: {movie_data[index]["Overview"]}</p>
        <form action="#" class="button" method="post">
            <input type="submit" name="page-change" value="Next"/>
            <input type="submit" name="page-change" value="Previous"/>
        </form>
    </body>
</html>
        '''
        html_code = html_code.encode("utf-8")
        page.write(html_code.decode("utf-8"))
        return page_url