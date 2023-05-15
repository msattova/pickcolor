

let file = document.getElementById('uploadimage');
let canvas = document.getElementById('canvas');
const canvasWidth = 400;
const canvasHeight = 300;
let uploadImgSrc;

// Canvasの準備
canvas.width = canvasWidth;
canvas.height = canvasHeight;
let canvasCtx = canvas.getContext('2d');

let targetPixel;

function _getPointColor(e) {
  targetPixel = canvasCtx.getImageData(e.offsetX, e.offsetY, 1, 1);
  console.log(targetPixel.data);
  console.log(`rgba(${targetPixel.data[0]}, ${targetPixel.data[1]}, ${targetPixel.data[2]}, ${targetPixel.data[3]})`);
};

canvas.addEventListener('mousedown', _getPointColor);

function getRGBColors(imageData) {
  let RGBColors = Array();
  for (let i = 0; i < imageData.length; i += 4){
    RGBColors.push([imageData[i], imageData[i+1], imageData[i+2]]);
  }
  RGBColors = [...new Set(RGBColors.map(JSON.stringify))].map(JSON.parse)
  return RGBColors;
}

function calcHSV(rgb) {
  if ( !Array.isArray(rgb) ){
    return null;
  }
  const tmp =  rgb.map(e => e/255);
  const xMax = Math.max(...tmp);
  const xMin = Math.min(...tmp);
  const v = xMax;
  const c = xMax - xMin;
  const s =  (v == 0) ? 0 : c/v;
  return {
    x: (s*100),
    y: (v*100)
  };
}


function loadLocalImage(e) {
  // ファイル情報を取得
  const fileData = e.target.files[0];

  // 画像ファイル以外は処理を止める
  if(!fileData.type.match('image.*')) {
    alert('画像を選択してください');
    return;
  }

  // FileReaderオブジェクトを使ってファイル読み込み
  const reader = new FileReader();
  // ファイル読み込みに成功したときの処理
  reader.onload = function() {
    // Canvas上に表示する
    //uploadImgSrc = reader.result;
    canvasDraw(reader.result);

  };

  // ファイル読み込みを実行
  reader.readAsDataURL(fileData);
}

// ファイルが指定された時にloadLocalImage()を実行
file.addEventListener('change', loadLocalImage, false);

// Canvas上に画像を表示する
function canvasDraw(uploadimage) {
  // canvas内の要素をクリアする
  //canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
  // Canvas上に画像を表示
  let img = new Image();
  //img.src = uploadImgSrc;
  img.src = uploadimage;
  img.onload = function() {
    console.log(this.width);
    canvas.height = this.height * (canvasWidth / this.width);
    canvasCtx.drawImage(img, 0, 0, canvas.width, canvas.height);

    // Chartjsで散布図を描画
    // ここでないとcanvas領域に画像が描画される前に実行されてしまう
    const imgdt = canvasCtx.getImageData(0, 0, canvas.width, canvas.height);
    const imageData = imgdt.data;
    console.log(canvas.height, canvas.width);

    drawChart(imageData);
  }
}


function drawChart(imageData) {
  const RGBColors = getRGBColors(imageData);
  const HSVdata = RGBColors.map(e => calcHSV(e));
  console.log(RGBColors);
  console.log(HSVdata);
  if (window.myChart) {
    window.myChart.destroy()
  }

  const ctx = document.getElementById('chart');
  window.myChart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        data: HSVdata
      }]
    },
    options:{
        plugins: {
          maintainAspectoRatio: false,
          legend: {
            display: false,
          },
        },
      scales: {
        x: {
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: {
            stepSize: 20,
          },
          title: {
            display: true,
            text: "彩度",
          }
        },
        y: {
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: {
            stepSize: 20,
          },
          title: {
            display: true,
            text: "明度",
          }
        }
      }
    }
  });
}

window.onload = () => {
  drawChart([]);
};
