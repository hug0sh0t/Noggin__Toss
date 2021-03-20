import React from 'react'
import {apiNogginCreate} from './lookup'


export function NogginCreate(props) {
  
  var encodedFileTransfer;
  var vidEncode;
  //var trueString;
  const {didNoggin} = props
  const textAreaRef = React.createRef()
  // const picRef = React.createRef()
    const handleBackendUpdate = (response, status) =>{
       if (status === 201) {
         didNoggin(response)
       } else if (status === 400) { 
         console.log(response," STATUS >>> ", status)
         alert("BAD FILE SENT")
        }else {
         console.log('not error 201',response)
         alert("NON 201")
       }
    }

  const encodeFile = (element) => {
    const [file] = element.target.files;
    const reader = new FileReader();
    reader.onloadend = function() {
      if (reader.result.includes("data:video/mp4")){
        vidEncode = reader.result
      } else if (reader.result.includes("data:image/jpeg"))
        encodedFileTransfer = reader.result
    }
    reader.readAsDataURL(file);
  }

  

  const handleSubmit = (event) => {
    event.preventDefault()
    const newVal = textAreaRef.current.value 
    apiNogginCreate(newVal, encodedFileTransfer, vidEncode, handleBackendUpdate)
    textAreaRef.current.value = ''
  }
 
  return <center className='col-12 mb-3'>
    <form className="mt-5" onSubmit={handleSubmit} encType="multipart/form-data">
      <center>  
        <textarea placeholder="Tossyanoggin ... " ref={textAreaRef} required={true} className='form-control mt-5' 
          style={{"resize": "none","width": "550px", "height":"100px","border":"none","backgroundColor":"#F1F1F1","boxShadow":"none"}}>
          </textarea>
        <label style={{"border":"none","padding":"0","background":"none","boxShadow":"none"}} className="zoom custom-file-upload mr-5">
          <img className="pointer" style={{"width":"55px","height":"55px"}} src='https://noggintoss.com/media/react/pic.png' alt='choice' />
          <input id='video' style={{"display":"none"}} onChange={encodeFile} type='file'/>
        </label>
        <button style={{"border":"none","padding":"0","background":"none","boxShadow":"none"}} type='submit' className='zoom myDIV btn btn-outline-light btn-lg my-3'>
          <img style={{"width":"55px","height":"55px"}} src='https://noggintoss.com/media/react/upload.png' alt='world' /></button>
        <center style={{"color":"#248f24","width":"150px","border":"0.5px solid #f1f1f1"}} className="hide badge badge-lg badge-pill badge-light">Create noggin?</center>
      </center>
    </form>
    
  </center>
}





