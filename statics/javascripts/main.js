(function () {
    vm = this;
    Dropzone.autoDiscover = false;    

    // Properties
    vm.imageUploader = new Dropzone('#image-uploader');

    // Methods
    vm.onLoad = onLoad;

    // Events
    vm.imageUploader.on('success', handleImageUploadSuccess);

    // ------------------- //
    function onLoad() {
        
    }

    // --------------------- //
    function handleImageUploadSuccess(originalImage, serverResponse) {
        let { faces, image } = serverResponse;
        let img = document.getElementById('result-image');

        img.src = `data:image/png;base64, ${image}`;

        $("#result-table > tbody").empty();        

        faces.forEach(function(face, i) {
            $('#result-table > tbody:last-child').append(`<tr><td>${i + 1}</td><td>${face}</td></tr>`);
        });

        if (faces.length === 0) {
            $('#result-table > tbody:last-child').append(`<tr><td></td><td>404 - faces not found.</td></tr>`);
        }
    }

})();
