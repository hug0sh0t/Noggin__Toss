import React, {useState} from 'react'
import { ActionBtn, SaluteBtn} from './buttons'

import {
  UserDisplay,
  UserPicture,
} from '../profiles'


export function ParentNoggin(props){
  const {noggin} = props
  return noggin.parent ? <Noggin isRelay relayer={props.relayer} hideActions className={' '} noggin={noggin.parent}/>: null
}

export function Noggin(props) {
  const {noggin, didRelay, hideActions, isRelay, relayer} = props
  const [actionNoggin, setActionNoggin] = useState(props.noggin ? props.noggin : null)
  let className = props.className ? props.className :'col-25 mx-auto col-md-6' 
  className = isRelay === true ? `${className} p-2` : className
  const path = window.location.pathname
  const match = path.match(/(?<nogginid>\d+)/) 
  const urlNogginId = match ? match.groups.nogginid : -1
  const isDetail = `${noggin.id}` === `${urlNogginId}`

  const handleLink = (event) => {
    event.preventDefault()
    window.location.href = `/${noggin.id}`
  }
  const handlePerformAction = (newActionNoggin, status) => {
    if (status === 200) {
      setActionNoggin(newActionNoggin)
    } else if (status === 201){
      if (didRelay) {
        didRelay(newActionNoggin)
      }
      // transfer to nogginlist
    }
  }

  return <center className={className}>
    <div>
      {isRelay === true && <div className='small container' style={{color: '#e6b800'}}>
        <div style={{"height":"80px"}}>
      <UserDisplay hideLink={true} user={noggin.user}/></div></div>}
      </div>     
      <div className=''>
        <div className='small'>
          {!relayer && <center><UserPicture user={noggin.user}/>
          </center>}
      </div>
        <div className='col-35'>
        <div>
          {!relayer && <small className="small" style={{"color":"#ff1a75"}}>
            <UserDisplay user={noggin.user}/></small>}</div>
        <span colSpan="" style={{"fontFamily":"Lucida Sans Unicode"}}>
          <div className="pointer" 
          onClick={handleLink} 
            style={{"width":"900px","wordWrap":"breakWord","overfloWrap":"breakWord","msWordBreak": "breakAll","wordBreak": "breakWord","whiteSpace":"preWrap"}}>{noggin.content}</div>
            </span>
        <br></br>
        
      <div className="container" style={{"display":"inlineBlock"}}>    
        {noggin.video &&  <center><video style={{"boxShadow":"none","outline":"none"}} className="shadow-lg responsive rounded" autoPlay muted width="620" height="360" controls="controls">
      <source src={noggin.video} type="video/mp4"></source>
      </video></center>}

        {!noggin.video && <img onClick={handleLink} className='pointer mr-5 mt-2 ml-5 shadow-lg rounded'
        style={{"width": "600px","height":"auto"}} src={noggin.image} alt=''/>}

       {isDetail === true ? null : 
         <button className='container btn btn-outline-dark btn-lg btn-block rounded' style = {{"width":"600px","border":"none"}} onClick={handleLink}>
           {noggin.comments}
            {noggin.comments === 1 ?  " Comment" :"  Comments"}
           <img style={{"width":"30px","height":"30px"}} className="ml-2"
             src="https://noggintoss.com/media/parking/comment.png" alt="lll"/>
           {noggin.eyeballs}
            {noggin.eyeballs === 1 ?  " Member View" :" Member Views"}
           <br></br></button>}
 
        {(actionNoggin && hideActions !== true) && <React.Fragment><div>
          <small><SaluteBtn noggin={actionNoggin} didPerformAction={handlePerformAction}
              action={{type: "like", display: noggin.likes === 1 ? "Salute" : "Salutes"}}/>
          <ActionBtn noggin={actionNoggin} didPerformAction={handlePerformAction}
          action={{type: "unlike", display:
            <img className="ml-3" style={{"width":"30px","height":"30px"}} alt='break' src="https://noggintoss.com/media/parking/ex.png"/>}}/></small>
          </div></React.Fragment>}

        <br></br>
        <small className='small'><small className="small"> created {noggin.timestamp}</small></small></div>
          
          <hr  style={{"width":"400px"}}></hr>
      </div>
    </div>
  </center>
}
