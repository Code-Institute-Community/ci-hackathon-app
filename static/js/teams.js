/*  */
let teams = JSON.parse(document.getElementById('_teams').textContent);
let leftover_participants = JSON.parse(document.getElementById('_leftover_participants').textContent);

addNewTeam();
confirmBeforeAction('.clear-teams-form', 'submit', 'Do you really want to clear all teams and re-distribute them?')
confirmBeforeAction('.distribute-teams-form', 'submit', 'Some participants have not been assigned to a team. Do you still want to proceed?')

function allowDrop(ev) {
    ev.preventDefault();
  }
  
function drag(ev) {
    ev.dataTransfer.setData('text', ev.target.id);
}

function drop(ev) {
    /* Drop event which triggers functions to update the team score and the
    team object used to create or edit the teams */
    console.log(ev.target.nodeName)
    let targetElement;
    ev.preventDefault();
    let data = ev.dataTransfer.getData('text');
    let movingElement = document.getElementById(data);
    let movingElementParent = movingElement.parentElement;
    if(ev.target.nodeName == 'LI') {
        targetElement = ev.target.parentElement.id;
        ev.target.parentElement.appendChild(movingElement);
    } else if(ev.target.nodeName == 'SPAN'){
        targetElement = ev.target.parentElement.parentElement.id;
        ev.target.parentElement.parentElement.appendChild(movingElement);
    } else if(ev.target.nodeName == 'H5') {
        targetElement = ev.target.nextElementSibling.id;
        ev.target.nextElementSibling.appendChild(movingElement);
    } else if(ev.target.nodeName == 'DIV') {
        targetElement = ev.target.children[1].id;
        console.log(ev.target.children[1])
        ev.target.children[1].appendChild(movingElement);
    }
    else {
        targetElement = ev.target.id;
        ev.target.appendChild(movingElement);
    }
    changeTeamData(movingElement, movingElementParent.id, targetElement);
    changeTeamScores(movingElement, movingElementParent.id, targetElement);
}

function changeTeamScores(movedElement, movedElementParentId, targetElementId){
    /* Deducts the participant's experience level from the 
    the overall score for the team the participant was previously part of
    and adds it to the new team's score */
    let movedLevel = parseInt(movedElement.dataset.level);
    if (targetElementId != 'leftover_participants'){
        let teamScoreSpan = document.getElementById(targetElementId +'_score');
        teamScoreSpan.innerText = parseInt(teamScoreSpan.innerText) + movedLevel;
        let removeScoreSpan = document.getElementById(movedElementParentId +'_score');
        if(removeScoreSpan != null) {
            removeScoreSpan.innerText = parseInt(removeScoreSpan.innerText) - movedLevel;   
        }   
    }
}

function changeTeamData(movedElement, movedElementParentId, targetElementId){
    /* Removes the participant from the team the participant was previously 
    part of and adds it to the new team in the team data object which is used
    to create or edit the teams */
    if (movedElementParentId == targetElementId) {
        return
    }
    let movedElementParent= document.getElementById(movedElementParentId);
    console.log(movedElementParent)

    let team = movedElementParentId.includes('leftover_participants')
                ? leftover_participants
                : teams[movedElementParentId];
    let targetTeam = targetElementId.includes('leftover_participants')
                    ? leftover_participants
                    : teams[targetElementId];
    let userid = movedElement.dataset.userid;
    let user = team.filter(x => x.userid == userid)[0];
    if(movedElementParentId.includes('leftover_participants')){
        leftover_participants = leftover_participants
                                    .filter(x => x.userid != userid);
    } else {
        teams[movedElementParentId] = teams[movedElementParentId]
                                        .filter(x => x.userid != userid);
    }
    targetTeam.push(user)
    $('input[name="teams"]').val(JSON.stringify(teams));
}

function addNewTeam(){
    $('.add-team').click(function(){
        let numTeams = $('.team').length;
        let teamName = `team_${numTeams+1}`;
        let teamDisplayName = `Team ${numTeams+1}`;
        let teamTemplate = `<section class="card shadow mb-3 mt-3">
        <div class="card-body">
            <h5 class="p-orange card-title">${teamDisplayName}
            <span style="float:right">Team Score: <span id="${teamName}_score">0</span>
            </span></h5>
            <ol class="team team-drop-area" id="${teamName}"
                ondrop="drop(event)" ondragover="allowDrop(event)"></ol>
        </div>
    </section>`;
        $('#team-list').append($(teamTemplate));
        teams[teamName] = [];
    });
}

function confirmBeforeAction(className, action, msg){
    $(className).on(action, function(event){
        
        if(leftover_participants.length > 0) {
            let confirm_msg = 'Some participants have not been assigned to a team. Do you still want to proceed?';
            let confirmation = window.confirm(msg);
            console.log(teams)
            if(!confirmation){
                event.preventDefault();
            }
        }
    });
}
