import { useState } from "react";
import "./styles.css";
export default function App() {
  const [file, setFile] = useState(null);
  const [compression, setCompression] = useState("Recommended Compression");
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }
    setLoading(true);
    setDownloadUrl("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("compression", compression);
      const res = await fetch("https://iekyww3lkj.execute-api.ap-south-1.amazonaws.com/upload", { /
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setDownloadUrl(data.downloadUrl);
    } catch (err) {
      console.log(err);
      alert("Upload failed");
    }
    setLoading(false);
  };
  return (
    <div className="container">
      <h1>Secure File Compressor</h1>
      <div className="card">
        <input
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx,image/*"
        />
        {/* Compression Level Selection */}
        <div className="compression-box">
          <p>Choose Compression Level:</p>
          <label>
            <input
              type="radio"
              value="Extreme Compression"
              checked={compression === "Extreme Compression"}
              onChange={(e) => setCompression(e.target.value)}
            />
            Extreme Compression
          </label>
          <label>
            <input
              type="radio"
              value="Recommended Compression"
              checked={compression === "Recommended Compression"}
              onChange={(e) => setCompression(e.target.value)}
            />
            Recommended Compression
          </label>
          <label>
            <input
              type="radio"
              value="Less compression"
              checked={compression === "Less compression"}
              onChange={(e) => setCompression(e.target.value)}
            />
            Less compression
          </label>
        </div>
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Compressing..." : "Compress File"}
        </button>
        {downloadUrl && (
          <div className="result">
            <a href={downloadUrl} target="_blank" rel="noreferrer">
              Download Compressed File
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
