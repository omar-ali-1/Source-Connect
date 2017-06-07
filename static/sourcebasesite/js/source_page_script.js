//$("#menu-list").remove();
//console.log("removed");
    
var dropdown = document.createElement('li');
dropdown.setAttribute('class', 'dropdown');
dropdown.innerHTML = document.getElementById('dropdown').innerHTML;
document.getElementById('menu-list').appendChild(dropdown);
//$("#navbar").append(dropdown);