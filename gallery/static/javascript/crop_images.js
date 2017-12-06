$(function () {
var bw_style = ".cropper-canvas, .cropper-wrap-box, .cropper-drag-box, .cropper-view-box{" + 
" WebkitFilter: grayscale(100%); filter: grayscale(100%);}"


  $("#id_image").change(function(){
    if(this.files && this.files[0]){
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#image").attr("src", e.target.result);
              
        $("#modalCrop").modal("show");
      }
      reader.readAsDataURL(this.files[0]);
    }
  });

  $("#id_profile_pic").change(function(){
    if(this.files && this.files[0]){
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#image").attr("src", e.target.result);
              
        $("#modalCrop").modal("show");
      }
      reader.readAsDataURL(this.files[0]);
    }
  });


  var $image = $("#image");
  var cropBoxData;
  var canvasData;
  $("#modalCrop").on("shown.bs.modal", function(){
    $image.cropper({
      viewMode: 1,
      aspectRatio: 1/1,
      minCropBoxWidth: 200,
      minCropBoxHeight: 200,
      ready: function(){
        $image.cropper("setCanvasData", canvasData);
        $image.cropper("setCropBoxData", cropBoxData); 
      }
    });
  }).on("hidden.bs.modal", function(){
    cropBoxData = $image.cropper("getCropBoxData");
    canvasData = $image.cropper("getCanvasData");
    $image.cropper("destroy");
  });

  $(".js-zoom-in").click(function(){
    $image.cropper("zoom", 0.1);
  });

  $(".js-zoom-out").click(function(){
    $image.cropper("zoom", -0.1);
  });

  $(".js-crop-and-upload").click(function(){
    var cropData = $image.cropper("getData");
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);

    if($("style.black-white").text() == "")
      $("#id_picFilter").val(0);
    else
      $("#id_picFilter").val(1);

    $("#formUpload").submit();
  });

  $(".black-white").click(function(){
    if($("style.black-white").text() == "")
      $("style.black-white").text(bw_style);
    else
      $("style.black-white").text("");
  });


});