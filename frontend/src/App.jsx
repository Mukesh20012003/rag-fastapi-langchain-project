import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const [contextUsed, setContextUsed] = useState([]);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingAsk, setLoadingAsk] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoadingUpload(true);
      setUploadMessage("");

      const response = await fetch("/upload-doc", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setUploadMessage(data.detail || "Upload failed.");
        return;
      }

      setUploadMessage(data.message || "File uploaded successfully.");
    } catch (error) {
      console.error("Upload error:", error);
      setUploadMessage("Backend server not running or not reachable.");
    } finally {
      setLoadingUpload(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer("Please enter a question.");
      return;
    }

    try {
      setLoadingAsk(true);
      setAnswer("");
      setContextUsed([]);

      const response = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (!response.ok) {
        setAnswer(data.detail || "Failed to get answer.");
        return;
      }

      setAnswer(data.answer || "No answer received.");
      setContextUsed(data.context_used || []);
    } catch (error) {
      console.error("Ask error:", error);
      setAnswer("Backend server not running or not reachable.");
    } finally {
      setLoadingAsk(false);
    }
  };

  return (
    <div className="container">
      <h1>RAG System</h1>
      <p className="subtitle">FastAPI + LangChain + React</p>

      <div className="card">
        <h2>Upload Document</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loadingUpload}>
          {loadingUpload ? "Uploading..." : "Upload File"}
        </button>
        {uploadMessage && <p className="message">{uploadMessage}</p>}
      </div>

      <div className="card">
        <h2>Ask a Question</h2>
        <textarea
          rows="4"
          placeholder="Enter your question here..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        ></textarea>
        <button onClick={handleAsk} disabled={loadingAsk}>
          {loadingAsk ? "Thinking..." : "Ask Question"}
        </button>
      </div>

      <div className="card">
        <h2>Answer</h2>
        <p>{answer || "No answer yet."}</p>
      </div>

      {contextUsed.length > 0 && (
        <div className="card">
          <h2>Context Used</h2>
          {contextUsed.map((item, index) => (
            <div key={index} className="context-box">
              {item}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;