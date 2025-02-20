/* jshint esversion: 8, jquery: true */
$(document).ready(function(){
    $('.edit-image').click(setUpoadImageType);
    filterUsersByHackathon();

    $('.delete').submit(function(event){
        let confirmation = confirm("Do you really want to remove this team member?");
        if(!confirmation){
            event.preventDefault();
        }
    });

    $('.remove_hackathon_participant').submit(function(event){
        let confirmation = confirm("Do you really want to remove this team member?");
        if(!confirmation){
            event.preventDefault();

        }
        else{
            let confirmationDropoff = confirm("Do you really want to mark this participant as a drop off?");
            if(confirmationDropoff){
                $(this).append('<input type="hidden" name="dropoffs" value="1" /> ');
            }
        }
    });

    $('.hackadmin-add-participant').click(function(){
        let participantId = $(this).data('participant-id');
        $('.participant_id').val(participantId);
    });

    $('.hackadmin-add-judge').click(function(){
        let judgeId = $(this).data('judge-id');
        $('.judge_id').val(judgeId);
    });

    $('#add_participant_hackathon_id').change(function(){
        let hackathonId = $(this).val();
        $(`.hackadmin-team-select`).hide();
        $(`#hackadmin-team-select-${hackathonId}`).show();
    });
    enableReviewsSlider();
    openCompetencyDifficultyInPopup();
    closePopup();
    toggleCompetencyAssessmentIcon();
});

function setUpoadImageType(){
    let imageType = $(this).data('imageType');
    let identifier = $(this).data('identifier');
    $('#image-upload-type').val(imageType);
    $('#image-upload-identifier').val(identifier);
}

function filterUsersByHackathon(){
    $('#hackathonFilter').change(function(){
        let userCount = 0;
        let elementValue = $(this).val();
        $('#usersTable tbody tr').each(function(){
            if(elementValue == '0'){
                $(this).removeClass('hide-row');
                userCount++;
            } else {
                if($(this).data('hackathons').split(',').includes(elementValue)){
                    $(this).removeClass('hide-row');
                    userCount++;
                } else {
                    $(this).addClass('hide-row');
                }
            }
        });
        $('#userCount').text(userCount);
    });

    $('.downloadTable').click(function(){
        let csvContent = '';
        let tableId = $(this).data('tableid');
        let rows = $(`#${tableId} tr:not(.hide-row)`);
        rows.each(function(){
            let tds = $(this).children();
            let rowText = [];
            tds.each(function(){
                rowText.push($(this).text().trim());
            });
            csvContent +=rowText.join(',') + '\n';
        });

        let link = document.createElement('a');
        link.id = 'download-csv';
        link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(csvContent));
        link.setAttribute('download', `${tableId}_${new Date().getTime()}.csv`);
        document.body.appendChild(link);
        document.querySelector('#download-csv').click();
        document.body.removeChild(link);
    });

    $('.downloadTeams').click(function(){
        let csvContent = '';
        let tableId = $(this).data('tableid');
        let rows = $(`#${tableId} tr:not(.hide-row)`);
        rows.each(function(){
            let tds = $(this).children();
            console.log(rows)
            let rowText = [];
            let c = 0
            tds.each(function(){
                if (c == 1){
                    rowText.push('"' + $(this).text().split('\n').map(x => x.trim()).filter(x => x != '').join('\n') + '"');
                } else {
                    rowText.push($(this).text().trim());
                }
                c++;
            });
            csvContent +=rowText.join(',') + '\n';
        });

        let link = document.createElement('a');
        link.id = 'download-csv';
        link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(csvContent));
        link.setAttribute('download', `${tableId}_${new Date().getTime()}.csv`);
        document.body.appendChild(link);
        document.querySelector('#download-csv').click();
        document.body.removeChild(link);
    });
}

function enableReviewsSlider(){
    $('.reviews-slider .next-step').click(function() {
        let active_elem = $('.reviews-content.active');
        let next_elem = active_elem.next();
        if (next_elem && next_elem.hasClass('reviews-content')) {
            active_elem.removeClass('active');
            next_elem.addClass('active');
            active_elem.hide();
            next_elem.hide().fadeIn();
        }
    });
    $('.reviews-slider .prev-step').click(function() {
        let active_elem = $('.reviews-content.active');
        let prev_elem = active_elem.prev();
        if (prev_elem && prev_elem.hasClass('reviews-content')) {
            active_elem.removeClass('active');
            prev_elem.addClass('active');
            active_elem.hide();
            prev_elem.hide().fadeIn();
        }
    });
}


function openCompetencyDifficultyInPopup(){
    $('#openCompetencyDifficultyPopup').click(function(){
        const params = `width=500,height=350,left=-1000,top=-1000`;
        const window_name = 'Create Competency Difficulty';
        window.open(create_competency_difficulty_url, window_name, params);
    })
}

function closePopup(){
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    let close_popup = urlParams.get('close_popup');
    if(close_popup){
        window.opener.location.reload();
        window.close();
    }
}

function toggleCompetencyAssessmentIcon() {
    $('.competency-assessment-radio').change(function(){
        let current_selection = $(this).parent().parent().parent().find('label i.fas');
        if(current_selection.length > 0){
            _changeClass(current_selection[0]);
        }
        let new_selection = $(this).parent().find('label i');
        _changeClass(new_selection[0]);
        _chageSelection($(this).data('form'), $(this).data('rating'));
    });
}

function _changeClass(element){
    if(element.classList.contains('fas')){
        element.classList.remove('fas');
        element.classList.add('far');
    } else {
        element.classList.remove('far');
        element.classList.add('fas');
    }
}


function _chageSelection(form_num, rating){
    $(`#id_form-${form_num}-rating`).val(rating);
}

// Modal for enlarging the badge when clicked
document.addEventListener('DOMContentLoaded', function() {
    $('#badgeModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var badgeUrl = button.data('badge-url');
        var modal = $(this);
        modal.find('#badgeModalImage').attr('src', badgeUrl);
    });
});