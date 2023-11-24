import { createContext, useState } from "react"
import { Event, hydrateClientStorage, useEventLoop } from "/utils/state.js"

export const initialState = {"auth_state": {"confirm_password": "", "password": "", "username": ""}, "home_state": {"REST_API_KEY": "", "clear_map1": [], "clear_map2": "", "clear_map3": {"columns": [], "data": []}, "clear_map4": "/map.html", "df": {"columns": [], "data": []}, "files": [], "followers": [], "following": [], "friend": "", "img": [], "locations": [], "map_html": "/map.html", "map_iframe": "<iframe src=\"/map.html\" width=\"100%\" height=\"600\"></iframe>", "map_iframe1": "<iframe src=\"/map.html\" width=\"100%\" height=\"600\"></iframe>", "map_search_check": false, "real_time_trend": {}, "search": "", "search_users": [], "show": false, "show_right": false, "show_top": false, "show_video": "", "tag_search": "", "tweet": "", "tweets": [], "video_search": "", "web_trend": {}}, "is_hydrated": false, "logged_in": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}, "user": null}

export const ColorModeContext = createContext(null);
export const StateContext = createContext(null);
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}}

export const initialEvents = () => [
    Event('state.hydrate', hydrateClientStorage(clientStorage)),
]

export const isDevMode = true

export function EventLoopProvider({ children }) {
  const [state, addEvents, connectError] = useEventLoop(
    initialState,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectError]}>
      <StateContext.Provider value={state}>
        {children}
      </StateContext.Provider>
    </EventLoopContext.Provider>
  )
}