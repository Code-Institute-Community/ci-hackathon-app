$(document).ready(function(){
    $('.edit-image').click(setUpoadImageType);
    filterUsersByHackathon();
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

    $('#downloadUsers').click(function(){
        let csvContent = '';
        let rows = $('#usersTable tr:not(.hide-row)');
        rows.each(function(){
            let tds = $(this).children();
            let rowText = [];
            tds.each(function(){
                rowText.push($(this).text().trim());
            });
            csvContent +=rowText.join(',') + '\n';
        });

        let link = document.createElement('a')
        link.id = 'download-csv'
        link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(csvContent));
        link.setAttribute('download', 'user-export.csv');
        document.body.appendChild(link);
        document.querySelector('#download-csv').click();
    });
}
