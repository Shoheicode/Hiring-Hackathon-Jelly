//import logo from './logo.svg';
import { unstable_renderSubtreeIntoContainer } from 'react-dom';
import './App.css';
import { useEffect, useState } from 'react';
import axios, { Axios } from "axios"

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

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(file)

    if (!file) {
      return;
    }
    const url = URL.createObjectURL(file);
    setSource(url)

    console.log(file.name)

    const formData = new FormData();
    formData.append('video', file); // videoFile is the MP4 file from an input

    const objectUrl = window.URL.createObjectURL(file);

    console.log(objectUrl)
  
    //console.log(formData);

    // fetch('https://httpbin.org/post', {
    //   method: 'POST',
    //   body: file,
    //   // 👇 Set headers manually for single file upload
    //   headers: {
    //     'content-type': file.type,
    //     'content-length': `${file.size}`, // 👈 Headers need to be a string
    //   },
    // })
    //   .then((res) => res.json())
    //   .then((data) => console.log(data))
    //   .catch((err) => console.error(err));

    try {
      const response = await fetch('http://127.0.0.1:5000/gam', {
        method: 'POST',
        headers: {
          "Content-Type": "multipart/form-data",
          'Access-Control-Allow-Origin':'*',
          'Access-Control-Allow-Methods':'POST'
        },
        body: formData,
      });
      
      if (response.ok) {
        console.log('Video uploaded successfully');
      } else {
        console.error('Upload failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

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
      <input onChange={
         (e) => {
           setFile(e.target.files[0]);
           console.log(e.target.files[0])
          }
       } type='file' name='video'/> 

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
      }
    </div>
  );
}

export default App;
