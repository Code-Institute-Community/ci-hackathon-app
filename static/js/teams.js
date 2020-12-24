const teams = JSON.parse(document.getElementById('teams').textContent);
const leftover_participants = JSON.parse(document.getElementById('leftover_participants').textContent);

console.log(teams)
console.log(leftover_participants)


function allowDrop(ev) {
    ev.preventDefault();
  }
  
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    console.log(ev)
    console.log(ev.target.parentElement)
    if(ev.target.nodeName == 'LI') {
        ev.target.parentElement.appendChild(document.getElementById(data));
    } else {
        ev.target.appendChild(document.getElementById(data));
    }
}