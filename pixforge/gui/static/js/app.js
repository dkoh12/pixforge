const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const previewWrap = document.getElementById("preview-wrap");
const dropPlaceholder = document.getElementById("drop-placeholder");
const previewImg = document.getElementById("preview-img");
const fileInfo = document.getElementById("file-info");
const convertBtn = document.getElementById("convert-btn");
const status = document.getElementById("status");

let selectedFile = null;

function loadFile(file) {
  if (!file || !file.type.startsWith("image/")) {
    setStatus("Please drop a valid image file.", "error");
    return;
  }
  selectedFile = file;
  const url = URL.createObjectURL(file);
  previewImg.src = url;

  const img = new window.Image();
  img.onload = () => {
    fileInfo.textContent = `${file.name} · ${img.naturalWidth}×${img.naturalHeight}px · ${(file.size / 1024).toFixed(1)} KB`;
  };
  img.src = url;

  dropPlaceholder.style.display = "none";
  previewWrap.style.display = "block";
  dropZone.classList.add("has-image");
  convertBtn.disabled = false;
  setStatus("");
}

fileInput.addEventListener("change", e => loadFile(e.target.files[0]));

dropZone.addEventListener("dragover", e => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", e => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  loadFile(e.dataTransfer.files[0]);
});

function setStatus(msg, type = "") {
  status.textContent = msg;
  status.className = type;
}

convertBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  convertBtn.disabled = true;
  setStatus("Converting...");

  const form = new FormData();
  form.append("image", selectedFile);
  form.append("format", document.getElementById("format").value);
  form.append("quality", document.getElementById("quality").value);
  form.append("scale", document.getElementById("scale").value);
  form.append("dpi", document.getElementById("dpi").value);
  form.append("width", document.getElementById("width").value);
  form.append("height", document.getElementById("height").value);
  form.append("rotate", document.getElementById("rotate").value);
  form.append("flip", document.getElementById("flip").value);
  form.append("grayscale", document.getElementById("grayscale").checked ? "true" : "false");

  try {
    const res = await fetch("/convert", { method: "POST", body: form });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Conversion failed");
    }

    const blob = await res.blob();
    const disposition = res.headers.get("Content-Disposition") || "";
    const match = disposition.match(/filename="?([^"]+)"?/);
    const filename = match ? match[1] : "converted_image";

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();

    setStatus(`✅ Downloaded as ${filename}`, "success");
  } catch (err) {
    setStatus(`❌ ${err.message}`, "error");
  } finally {
    convertBtn.disabled = false;
  }
});
