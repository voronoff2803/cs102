<!DOCTYPE html>
<html>
<style>
body {
padding: 0px 0px 0px;
background-color: whitesmoke;
font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
color: #333;
font-size: 14px;
line-height: 20px;
}

.w-col {
position: relative;
float: left;
/* width: 100%; */
min-height: 1px;
/* padding-left: 10px; */
/* padding-right: 10px; */
}

.w-col-3 {
width: 25%;
}

.swatch_column {
margin-bottom: 40px;
padding-right: 16px;
padding-left: 16px;
}

.swatch_block {
    width: 293px;
    height: 400px;
    border-radius: 6px;
    box-shadow: rgba(219, 219, 219, 0.56) 0px 3px 8px 0px;
    -webkit-transform: none;
    -ms-transform: none;
    transform: none;
    -webkit-transition: all 500ms ease;
    transition: all 500ms ease;
    color: white;
    background-color: white;
}

.gradient_swatch_1 {
    height: 220px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    background-color: #787878;
}

.swatch_name {
    width: 243px;
    position: absolute;
    bottom: 20px;
    margin-left: 0px;
    padding: 0px 25px 0px;
    background-color: white;
    font-family: proxima-nova-soft, sans-serif;
    color: gray;
    font-size: 15px;
    font-weight: 500;
}

.swatch_value {
    padding: 30px 25px 30px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    background-color: white;
    font-family: proxima-nova-soft, sans-serif;
    color: gray;
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
}





.btn-pomegranate
{
  width: 150px;
  height:45px;
  background-color:#D14233;
  color: white;

  &:hover
  {
    background-color:#EA6153;
    color: white;
  }
  .glyphicon
  {
    color:white;
  }
}

.btn {
    background-color: white; /* Blue background */
    border: none; /* Remove borders */
    color: gray; /* White text */
    padding: 0px 0px; /* Some padding */
    font-size: 20px; /* Set a font size */
    cursor: pointer; /* Mouse pointer on hover */
}

.btnr {
    background-color: white; /* Blue background */
    border: none; /* Remove borders */
    color: gray; /* White text */
    padding: 0px 0px 0px 185px; /* Some padding */
    font-size: 20px; /* Set a font size */
    cursor: pointer; /* Mouse pointer on hover */
}

.swatch_details{
    padding: 0px 0px;
}
ul {
    list-style-type: none;
    margin: 0px 0px 60px 0px;
    padding: 0;
    overflow: hidden;
    text-transform: uppercase;
}
li {
    float: left;
}
li a {
    display: block;
    color: gray;
    text-align: center;
    padding: 24px 16px;
    text-decoration: none;
}
li a:hover:not(.active) {
    color: #111;
}
.active {
    color: #4CAF50;
}


A {
    text-decoration: none;
    color: gray;
   }
A:hover {
    color: black;
   }
</style>
<head>
<ul>
  <li><a href="/news" class="active" >All news</a></li>
  <li><a href="/recommendations" >Recommendations</a></li>
  <li><a href="/update_news" >Add some news</a></li>
  <li><a href="/getrecommendations" >Get recommendations</a></li>
</ul>
</head>
<body>
<script defer src="https://use.fontawesome.com/releases/v5.0.6/js/all.js"></script>
%for row in rows:
<div class="w-section main_body">
        <div class="w-col swatch_column">
            <div class="swatch_block">
                <div class="gradient_swatch_1">
                    <img class="gradient_swatch_1" src="{{row.img}}" >
                </div>
                <div class="swatch_details">
                    <div  class="swatch_value"><a class="A" href="{{row.url}}">{{row.title}}</a></div>
                    <div class="swatch_name">
                    <a class="btn" href="/add_label/?label=good&id={{row.id}}"><i class="fas fa-heart"></i></a>
                    <a class="btnr" href="/add_label/?label=never&id={{row.id}}"><i class="fas fa-trash-alt"></i></a>
                    </div>
                </div>
            </div>
        </div>
</div>
%end
</body>
</html>