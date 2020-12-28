const teams = JSON.parse(document.getElementById('teams').textContent);
const leftover_participants = JSON.parse(document.getElementById('leftover_participants').textContent);


function allowDrop(ev) {
    ev.preventDefault();
  }
  
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    let targetElement;
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    if(ev.target.nodeName == 'LI') {
        targetElement = ev.target.parentElement.id;
        ev.target.parentElement.appendChild(document.getElementById(data));
    } else {
        targetElement = ev.target.id;
        ev.target.appendChild(document.getElementById(data));
    }
<<<<<<< HEAD
    moveTeamData(data, targetElement)
}

function moveTeamData(movedElement, targetElement){
    console.log(movedElement)
    console.log(targetElement)
    let fromGroup = movedElement.split('-')[0];
    let fromIndex = movedElement.split('-')[1];
    let toGroup = targetElement;
    console.log(fromIndex)
    if(fromGroup == 'leftover_participants') {
        let a = leftover_participants.splice(fromIndex, 1);
        console.log(leftover_participants)
    }
=======
    moveTeamData(data, targetElement);
}

function moveTeamData(movedElementId, targetElementId){
    let movedElement = document.getElementById(movedElementId);
    let targetElement = document.getElementById(targetElementId);
    console.log(`Moved Element: ${movedElement.id}`)
    console.log(`Dropped into Element: ${targetElement.id}`)
    
    /*let movedLevel = parseInt(movedElement.dataset.level);
    console.log(movedLevel)
    let teamScoreSpan = document.getElementById(targetElement+'_score');
    teamScoreSpan.innerText = parseInt(teamScoreSpan.innerText) + movedLevel;
    if(movedElement.id.includes('team')) {
        console.log("Moved from team")
        let removeScoreFromTeam = movedElement.parentNode.id;
        console.log(removeScoreFromTeam)
        let removeScoreSpan = document.getElementById(removeScoreFromTeam+'_score');
        removeScoreSpan.innerText = parseInt(removeScoreSpan.innerText) - movedLevel;
    }*/
>>>>>>> Adding team distribution template and javascript
}