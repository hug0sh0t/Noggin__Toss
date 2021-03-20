import React, {useEffect, useState} from 'react'

import {NogginCreate} from './create'
import {Noggin} from './detail'
import {apiNogginDetail} from './lookup'
import {NogginsList} from './list'
import {FeedList} from './feed'

export function FeedComponent(props) {
  const [newNoggins, setNewNoggins] = useState([])
  const canNoggin = props.canNoggin === "false" ? false : true
  const handleNewNoggin = (newNoggin) => {
     let tempNewNoggins = [...newNoggins]
     tempNewNoggins.unshift(newNoggin)    
     setNewNoggins(tempNewNoggins)
  }
  return <div className={props.className}>
          {canNoggin === true && <NogginCreate didNoggin={handleNewNoggin}  className='col-12 mb-3'/>}
        <FeedList  newNoggins={newNoggins} {...props} />
  </div>
}

export function NogginsComponent(props) {
  const [newNoggins, setNewNoggins] = useState([])
  const canNoggin = props.canNoggin === "false" ? false : true
  const handleNewNoggin = (newNoggin) => {
     let tempNewNoggins = [...newNoggins]
     tempNewNoggins.unshift(newNoggin)    
     setNewNoggins(tempNewNoggins)
  }
  return <div className={props.className}>
          {canNoggin === true && <NogginCreate didNoggin={handleNewNoggin} className='col-12 mb-3'/>}
        <NogginsList newNoggins={newNoggins} {...props} />
  </div>
}


export function NogginDetailComponent(props) {
  const {nogginId} = props
  const [didLookup, setDidLookup] = useState(false)
  const [noggin, setNoggin] = useState(null)

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setNoggin(response)
    } else {
      alert("There was an error finding your Noggin :/ ")
    }
  }
  useEffect(() =>{
    if (didLookup === false) {
      apiNogginDetail(nogginId, handleBackendLookup)
      setDidLookup(true)
    }
  },[nogginId, didLookup, setDidLookup])

  return noggin === null ? null : <Noggin noggin={noggin} className={props.className}/>
}


