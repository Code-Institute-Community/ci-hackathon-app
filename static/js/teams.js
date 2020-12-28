let teams = JSON.parse(document.getElementById('_teams').textContent);
let leftover_participants = JSON.parse(document.getElementById('_leftover_participants').textContent);

addNewTeam();

function allowDrop(ev) {
    ev.preventDefault();
  }
  
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    let targetElement;
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text");
    let movingElement = document.getElementById(data);
    let movingElementParent = movingElement.parentElement;
    if(ev.target.nodeName == 'LI') {
        targetElement = ev.target.parentElement.id;
        ev.target.parentElement.appendChild(movingElement);
    } else {
        targetElement = ev.target.id;
        ev.target.appendChild(movingElement);
    }

    changeTeamData(movingElement, movingElementParent.id, targetElement);
    changeTeamScores(movingElement, movingElementParent.id, targetElement);
}

function changeTeamScores(movedElement, movedElementParentId, targetElementId){
    let movedLevel = parseInt(movedElement.dataset.level);

    if (targetElementId != 'leftover_participants'){
        let teamScoreSpan = document.getElementById(targetElementId +'_score');
        teamScoreSpan.innerText = parseInt(teamScoreSpan.innerText) + movedLevel;
    }

    if(movedElement.id.includes('team')) {
        let removeScoreSpan = document.getElementById(movedElementParentId +'_score');
        removeScoreSpan.innerText = parseInt(removeScoreSpan.innerText) - movedLevel;
    }
}

function changeTeamData(movedElement, movedElementParentId, targetElementId){
    /*
    1) Get user from original team or leftover_participants
    2) Add it to new team
    3) Remove it from old team
    */
    let team = movedElementParentId.includes('team') ? teams[movedElementParentId] : leftover_participants;
    let targetTeam = targetElementId.includes('team') ? teams[targetElementId] : leftover_participants;
    let userid = movedElement.dataset.userid;
    let user = team.filter(x => x.userid == userid)[0];
    targetTeam.push(user)

    if(movedElementParentId.includes('team')){
        teams[movedElementParentId] = teams[movedElementParentId].filter(x => x.userid != userid);
    } else {
        leftover_participants = leftover_participants.filter(x => x.userid != userid);
    }
}

function addNewTeam(){
    $('.add-team').click(function(){
        let numTeams = $('.team').length;
        let teamName = `team_${numTeams+1}`;
        let teamDisplayName = `Team ${numTeams+1}`;
        let teamTemplate = `<section class="card shadow mb-3 mt-3">
        <div class="card-body">
            <h5 class="p-orange card-title">${teamDisplayName}<span style="float:right">Team Score: <span id="${teamName}_score">0</span></span></h5>
            <ol class="team team-drop-area" id="${teamName}" ondrop="drop(event)" ondragover="allowDrop(event)"></ol>
        </div>
    </section>`;
        $('#team-list').append($(teamTemplate));
        teams[teamName] = [];
    });
}

function distributeTeams(){
    $('.distribute-teams').click(function(){
        
    });
}