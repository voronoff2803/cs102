<style>
body {
  width: 85%;
  margin: auto;
  color: $text;
  font: 16px/1 'Open Sans', sans-serif;
  background: $bg;
  font-family: -apple-system, BlinkMacSystemFont,
    "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell",
    "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
  text-decoration: none;
  color: #404040;
  font-weight: 100;
  font-size: 16px;
}
table {
  background: #FFFFFF;
  box-shadow: 0 2px 11px 0 rgba(0,0,0,0.50);
  border-radius: 8px;
  border-collapse: collapse;
  width: 100%;
}

th, td {
    text-align: left;
    font-weight: 300;
    padding: 8px;
    text-transform: lowercase;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
    font-size: 120%;
    text-align: center;
    background-color: #999999;
    color: white;
    padding: 20px 8px;
    text-transform: uppercase;
}


.cool-link {
    display: inline-block;
    color: #000;
    text-decoration: none;
}

.cool-link::after {
    content: '';
    display: block;
    width: 0;
    height: 2px;
    background: #000;
    transition: width .3s;
}

.cool-link:hover::after {
    width: 100%;
    //transition: width .3s;
}

.button {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 16px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    -webkit-transition-duration: 0.4s; /* Safari */
    transition-duration: 0.4s;
    cursor: pointer;
}

.button5:hover {
    background-color: #555555;
    color: white;
}
ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 24px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: #111;
}

.active {
    background-color: #4CAF50;
}
</style>
<head>
<ul>
  <li><a href="/news" class="active" >All news</a></li>
  <li><a href="/recommendations" >Recommendations</a></li>
</ul>
</head>
<body>
<table class="rwd-table">
    <tr>
        <th>Fresh hacker news</th>
        <th>Author</th>
        <th>Likes</th>
        <th colspan="3">Rating</th>
    </tr>
    %for row in rows:
        <tr>
            <td><a class="cool-link" href="{{row.url}}">{{row.title}}</a></td>
            <td>{{row.author}}</td>
            <td>{{row.points}}</td>
            <td><a class="cool-link" href="/add_label/?label=good&id={{row.id}}">👍</a></td>
            <td><a class="cool-link" href="/add_label/?label=maybe&id={{row.id}}">😐</a></td>
            <td><a class="cool-link" href="/add_label/?label=never&id={{row.id}}">👎</a></td>
        </tr>
    %end
</table>
<br />
<a href="/update_news" class="button button5">I Wanna more HACKER NEWS!</a>
</body>