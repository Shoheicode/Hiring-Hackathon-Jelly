//import logo from './logo.svg';
import { unstable_renderSubtreeIntoContainer } from 'react-dom';
import './App.css';
import { useEffect, useState} from 'react';
import axios, { Axios } from "axios"
//const fs = require('fs');

function App() {
  const [data, setData] = useState("");

  const getData = async () =>{
    const response = await axios.get("http://127.0.0.1:5000/members")
    console.log(response)
    setData(response.data)
  }

  useEffect(()=>{
    getData()
  },[]);


  const sendData = async () =>{
    console.log("HIHfojdlajkflds")
    const url = "http://127.0.0.1:5000/login"

    const options = {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          'Access-Control-Allow-Origin':'*',
          'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'
      },
      body: JSON.stringify({
        name: "hihihih"
      })
  }

    fetch(url, options).
      then(response => response.json())
      .then(data => setData(data["message"]));
    
  }
  useEffect(() =>{
    sendData()
  }, [])

  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState({started: false, pc: 0})
  const [msg, setMsg] = useState(null)
  const [da, setFormData] =  useState(null)
  const [url, setSource] = useState(null)

  function VideoUploader() {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
      setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!file) {
        alert("Please select a file first!");
        return;
      }

      const formData = new FormData();
      formData.append("video", file);

      console.log(file)
      const filename = file.name

      
      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          console.log(response)
          const result = await response.json();
          console.log("Success:", result);
          // Handle success (e.g., show a success message)
        } else {
          console.error("Error:", response.statusText);
          // Handle error (e.g., show an error message)
        }
      } catch (error) {
        console.error("Error:", error);
        // Handle error (e.g., show an error message)
      }


      //const filename = file.name
      try {
        const response = await fetch(`http://localhost:5000/uploads/${filename}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get the filename from the Content-Disposition header if available
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameFromHeader = contentDisposition
          ? contentDisposition.split('filename=')[1].replace(/['"]/g, '')
          : filename;
  
        // Get the blob from the response
        const blob = await response.blob();
        
        // Create a temporary URL for the blob
        const url = window.URL.createObjectURL(blob);
        
        // Create a temporary anchor element and trigger the download
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filenameFromHeader;
        document.body.appendChild(a);
        a.click();
        
        // Clean up
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } catch (error) {
        console.error('Download failed:', error);
      }
    };

    return (
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="video/*" />
        <button type="submit">Upload Video</button>
      </form>
    );
  }
  

 // console.log(data[0])

  // const [file, setFile] = useState(null);
  // const [progress, setProgress] = useState({started: false, pc: 0})
  // const [msg, setMsg] = useState(null)

  // function handleUpload(){
  //   if(!file){
  //     console.log("No file selected")
  //   }

  //   const fd = new FormData()
  //   fd.append('file', file)
  //   console.log("JJOJO" +fd)

  //   axios.post('http://httpbin.org/post', fd, {
  //     onUploadProgress: (progressEvent) => {console.log(progressEvent.progress *100)},
  //     headers: {
  //       "Custom-Header": "value",
  //     }
  //   }).then(res => {
  //     setMsg("Upload successful")
  //     console.log(res.data)
  //   })
  //   .catch(err => console.log(err));
  // }

  // return (
  //   <div className="App">
  //     {/* <header className="App-header">
  //       <img src={logo} className="App-logo" alt="logo" />
  //       <p>
  //         Edit <code>src/App.js</code> and save to reload.
  //       </p>
  //       <a
  //         className="App-link"
  //         href="https://reactjs.org"
  //         target="_blank"
  //         rel="noopener noreferrer"
  //       >
  //         Learn React
  //       </a>
  //     </header> */}
  //     <h1>
  //       Uploading Files in React
  //     </h1>

  //     <input onChange={
  //        (e) => {
  //         setFile(e.target.files[0]);
  //        }
  //     } type='file'/> 

  //     <button onClick={handleUpload}>
  //       Upload
  //     </button>

  //   </div>
  // );

  
  // useEffect(() => {
  //   // Fetch data from the backend
  //   fetch('http://127.0.0.1:5000/members')
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setData(data);
  //       console.log(data);
  //     });
  // }, []);

  return (
    <div>
      <h1>Data from the Backend:</h1>

      {
        data
      }
      <VideoUploader />
      {/* <input onChange={
         (e) => {
           setFile(e.target.files[0]);
           console.log(e.target.files[0])
          }
       } type='file' name='video/*'/> 

       <button onClick={handleSubmit}>
          Upload
       </button>

      {url && (
        <video
          className="VideoInput_video"
          width="100%"
          height={"800px"}
          controls
          src={url}
        />
      )}
      {
        console.log(da)
      } */}
    </div>
  );
}

export default App;
