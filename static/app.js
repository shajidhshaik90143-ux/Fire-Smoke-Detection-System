const $ = id => document.getElementById(id);
const video = $("video");
const canvas = $("canvas");
const resultImage = $("resultImage");
let stream = null, timer = null, busy = false;

function update(result) {
  $("status").textContent = result.status;
  $("fireScore").textContent = Number(result.fire_score || 0).toFixed(2);
  $("smokeScore").textContent = Number(result.smoke_score || 0).toFixed(2);
  $("detections").textContent = (result.detections || []).length;
  $("systemStatus").textContent =
    result.status === "CRITICAL" ? "CRITICAL ALERT" :
    result.status === "WARNING" ? "WARNING" : "SYSTEM READY";

  const lines = (result.detections || []).map(d =>
    `${d.label} | score=${d.score} | bbox=${d.bbox.join(", ")}`
  );
  $("details").textContent = lines.length ? lines.join("\n") : "No significant detection.";
}

async function analyzeFrame() {
  if (!stream || busy) return;
  busy = true;
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

  const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg", .78));
  const fd = new FormData();
  fd.append("frame", blob, "frame.jpg");

  try {
    const res = await fetch("/api/frame", {method:"POST", body:fd});
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    update(data);
    resultImage.src = "data:image/jpeg;base64," + data.image;
  } catch (e) { console.error(e); }
  finally { busy = false; }
}

$("startBtn").onclick = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({video:true, audio:false});
    video.srcObject = stream;
    timer = setInterval(analyzeFrame, 700);
  } catch (e) {
    alert("Camera permission was denied or no camera is available.");
  }
};

$("stopBtn").onclick = () => {
  if (timer) clearInterval(timer);
  timer = null;
  if (stream) stream.getTracks().forEach(t => t.stop());
  stream = null;
  video.srcObject = null;
};

$("analyzeBtn").onclick = async () => {
  const file = $("imageFile").files[0];
  if (!file) return alert("Select an image first.");
  const fd = new FormData();
  fd.append("file", file);
  const data = await (await fetch("/api/analyze", {method:"POST", body:fd})).json();
  if (data.error) return alert(data.error);
  update(data);
  $("uploadedPreview").src = "data:image/jpeg;base64," + data.image;
};

$("videoBtn").onclick = async () => {
  const file = $("videoFile").files[0];
  if (!file) return alert("Select a video first.");
  $("videoResult").textContent = "Processing...";
  const fd = new FormData();
  fd.append("file", file);
  const data = await (await fetch("/api/video", {method:"POST", body:fd})).json();
  if (data.error) return $("videoResult").textContent = data.error;
  $("videoResult").textContent =
    JSON.stringify(data.summary, null, 2) +
    `\n\nProcessed file: /uploads/${data.processed_video}`;
};
