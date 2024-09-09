import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function App() {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(true);
  const [message, setMessage] = useState("");
  const [plotdata, setPlotdata] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      setIsLoading(true)
      const response = await axios.post("http://localhost:8000/uploadfile/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setError(false);
      setMessage(response.data.message);
      setPlotdata(response.data.plotdata);
      console.log(response);
      console.log(response.data);
      console.log(response.data.message);
      console.log(response.data.plotdata);
    } catch (error) {
      console.error("Error uploading file:", error);
      setError(true);
      setMessage("Error uploading file");
    } finally {
      setIsLoading(false)
    }
  };

  return (
    <div className="App">
      <h1>Upload a CSV File</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {error && <p>Ошибка!!!</p>}
      {isLoading && <p>Загрузка ...</p>}
      {message && <p>{message}</p>}
      {plotdata && console.log(plotdata.data)}
      {
      !error && !isLoading && 
      <Plot
        data={
          [
          plotdata.data,
          plotdata.prediction
          ]
        }

      />
      }
    </div>
  );
}

export default App;