
// crop-btn is the id of button that will trigger the event of change original file with cropped file.
const crop_btn = document.getElementById('crop-btn');

const height_box = document.getElementById('height')
const width_box = document.getElementById('width')
const x_cod_box = document.getElementById('x_cod')
const y_cod_box = document.getElementById('y_cod')


const image = document.getElementById('image');

console.log("its working");
  // Creating a croper object with the cropping view image
  // The new Cropper() method will do all the magic and diplay the cropping view and adding cropping functionality on the website
  // For more settings, check out their official documentation at https://github.com/fengyuanchen/cropperjs


const cropper = new Cropper(image, {
  autoCrop: true,
  viewMode: 1,
  scalable: false,
  zoomable: false,
  movable: true,
  minCropBoxWidth: 10,
  minCropBoxHeight: 10,

  crop(event) {
    x_cod_box.value = parseInt(event.detail.x);
    y_cod_box.value = parseInt(event.detail.y);
    width_box.value = parseInt(event.detail.width);
    height_box.value = parseInt(event.detail.height);
  },
});
