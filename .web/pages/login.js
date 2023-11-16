import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Button, Container, Heading, Image, Input, Link, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Text, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import NextLink from "next/link"
import NextHead from "next/head"



export default function Component() {
  const state = useContext(StateContext)
  const router = useRouter()
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)
  const focusRef = useRef();
  
  // Main event loop.
  const [addEvents, connectError] = useContext(EventLoopContext)

  // Set focus to the specified element.
  useEffect(() => {
    if (focusRef.current) {
      focusRef.current.focus();
    }
  })

  // Route after the initial page hydration.
  useEffect(() => {
    const change_complete = () => addEvents(initialEvents())
    router.events.on('routeChangeComplete', change_complete)
    return () => {
      router.events.off('routeChangeComplete', change_complete)
    }
  }, [router])


  return (
    <Fragment>
  <Fragment>
  {isTrue(connectError !== null) ? (
  <Fragment>
  <Modal isOpen={connectError !== null}>
  <ModalOverlay>
  <ModalContent>
  <ModalHeader>
  {`Connection Error`}
</ModalHeader>
  <ModalBody>
  <Text>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {getEventURL().href}
</Text>
</ModalBody>
</ModalContent>
</ModalOverlay>
</Modal>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Container centerContent={true} sx={{"maxWidth": "auto", "maxHeight": "auto", "height": "100vh", "bg": "url('aurora.jpg')"}}>
  <Container sx={{"height": "200px"}}/>
  <VStack sx={{"width": "500px", "height": "auto", "centerContent": true, "borderRadius": "20px", "boxShadow": "9px 9px 50px #ceddf5"}}>
  <Heading sx={{"display": "flex", "flexDirection": "column", "alignItems": "center", "textAlign": "center"}}>
  <Text sx={{"fontSize": "40px", "fontWeight": "bolder", "letterSpacing": "5px", "fontFamily": "Open Sans,Sans-serif", "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)", "-webkit-background-clip": "text", "color": "transparent", "centerContent": true}}>
  {`Aurora!`}
</Text>
</Heading>
  <Text sx={{"color": "gray.500", "fontWeight": "medium"}}>
  {`Create a picture with your story!`}
</Text>
  <Container centerContent={true}>
  <Container sx={{"height": "30px"}}/>
  <Image alt={`star`} src={`C:/Users/a/Desktop/vscodeGithub/aurora/assets/favicon.ico`} sx={{"width": "100px", "height": "100px"}}/>
</Container>
  <Container>
  <VStack>
  <Container centerContent={true} sx={{"alignItems": "left", "bg": "white", "border": "1px solid #eaeaea", "p": 4, "maxWidth": "400px", "borderRadius": "lg"}}>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_username", {value:_e0.target.value})], (_e0), {})} placeholder={`Username`} sx={{"mb": 4}} type={`text`}/>
  <Input onBlur={(_e0) => addEvents([Event("state.auth_state.set_password", {value:_e0.target.value})], (_e0), {})} placeholder={`Password`} sx={{"mb": 4}} type={`password`}/>
  <Button onClick={(_e) => addEvents([Event("state.auth_state.login", {})], (_e), {})} sx={{"bg": "blue.500", "color": "white", "_hover": {"bg": "blue.600"}}}>
  {`Log in`}
</Button>
</Container>
  <Text sx={{"color": "gray.600"}}>
  {`Don't have an account yet? `}
  <Link as={NextLink} href={`/signup`} sx={{"color": "blue.500"}}>
  {`Sign up here.`}
</Link>
</Text>
</VStack>
</Container>
</VStack>
</Container>
  <NextHead>
  <title>
  {`Reflex App`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
