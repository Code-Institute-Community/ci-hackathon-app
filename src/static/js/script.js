$(document).ready(function(){
    $('.edit-image').click(setUpoadImageType);
});

function setUpoadImageType(){
    let imageType = $(this).data('imageType');
    let identifier = $(this).data('identifier');
    $('#image-upload-type').val(imageType);
    $('#image-upload-identifier').val(identifier);
}
