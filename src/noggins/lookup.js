import {backendLookup} from '../lookup'

// master controls 
export function apiNogginCreate(newNoggin, newPic, newVid, callback) {
  const data = {content: newNoggin, image: newPic, video: newVid}
  backendLookup("POST", "/noggins/create/", callback, data)
}

export function apiNogginAction(nogginId, action , callback) {
  const data = {id: nogginId, action: action} 
  backendLookup("POST", "/noggins/action/", callback, data)
}


export function apiNogginDetail(nogginId, callback) {  
  backendLookup("GET", `/noggins/${nogginId}/`, callback)
}


export function apiNogginFeed(callback, nextUrl) {  
  let endpoint = "/noggins/feed/"
  if (nextUrl !== null && nextUrl !== undefined) {
    endpoint = nextUrl.replace("https://noggintoss.com/api", "")
  }
    backendLookup("GET", endpoint, callback)
}


export function apiNogginList(username, callback, nextUrl) {  
  let endpoint = "/noggins/"
  if (username) {
    endpoint = `/noggins/?username=${username}`
  }
  if (nextUrl !== null && nextUrl !== undefined) {
    endpoint = nextUrl.replace("https://noggintoss.com/api", "")
  }
    backendLookup("GET", endpoint, callback)
}

