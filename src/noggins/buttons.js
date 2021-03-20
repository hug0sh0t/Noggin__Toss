import React from 'react'

import {apiNogginAction} from './lookup'

export function ActionBtn (props) {
  const {noggin, action, didPerformAction} = props
  const likes = noggin.likes ? noggin.likes : 0 
  const className = props.className ? props.className : 'zoom btn btn-outline-danger btn-inline-block mt-4'
  const actionDisplay = action.display ? action.display : 'Action'
  //var pathConvert

  const handleActionBackendEvent = (response, status) =>{
    console.log(response, status)
    if ((status === 200 || status === 201) && didPerformAction) {
      didPerformAction(response, status)
    } else if (status === 400) {
      console.log("MISSING NEEDED CONTENT")
    }
  }

  const handleClick = (event) => {
    event.preventDefault()
  
    apiNogginAction(noggin.id, action.type, handleActionBackendEvent)
  }
  const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
  return <button className={className} 
    style={{"boxShadow":"none","border":"none","padding":"0","background":"none"}} onClick={handleClick}>{display} </button>
}

export function SaluteBtn (props) {
  const {noggin, action, didPerformAction} = props
  const likes = noggin.likes ? noggin.likes : 0 
  const className = props.className ? props.className : 'btn btn-warning btn-inline-block mt-4'
  const actionDisplay = action.display ? action.display : 'Action'
  //var pathConvert

  const handleActionBackendEvent = (response, status) =>{
    console.log(response, status)
    if ((status === 200 || status === 201) && didPerformAction) {
      didPerformAction(response, status)
    } else if (status === 400) {
      console.log("MISSING NEEDED CONTENT")
    }
  }
  const handleClick = (event) => {
    event.preventDefault()
    apiNogginAction(noggin.id, action.type, handleActionBackendEvent)
  }
  const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
  return <button className={className} 
    style={{"boxShadow":"none","border":"none","padding":"0","background":"none"}} onClick={handleClick}>
    <h4><img className="zoom mr-3" 
      style={{"height":"70px","width":"70px","border":"none","background":"none","padding":"0"}} src="http://104.131.85.52/media/parking/cckk.png" alt=''/>
    {display}</h4>
    
    </button>
}

