import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, set_val, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Box, Button, ButtonGroup, Center, Heading, Input, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, option, Select, Text, Tooltip, useColorMode, VStack } from "@chakra-ui/react"
import { ArrowBackIcon } from "@chakra-ui/icons"
import NextHead from "next/head"



export default function Component() {
  const state = useContext(StateContext)
  const router = useRouter()
  const { colorMode, toggleColorMode } = useColorMode()
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
    const change_complete = () => addEvents(initialEvents.map((e) => ({...e})))
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
  <Text sx={{"fontSize": ["100%", "115%", "130%", "135%", "125%"], "fontFamily": "Helvectica", "transition": "all 650ms ease", "textAlign": "center"}}>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {`http://localhost:8000`}
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
  <Center sx={{"paddingTop": "10em"}}>
  <VStack sx={{"boxShadow": "lg", "bg": "", "padding": "1em", "border": "1px solid #ddd", "borderRadius": "25px"}}>
  <Heading sx={{"fontSize": ["250%", "275%", "300%", "325%", "350%"], "textAlign": "center", "transition": "all 650ms ease"}}>
  {`Audit Details`}
</Heading>
  <Input onBlur={(_e0) => addEvents([Event("state.set_customer_name", {value:_e0.target.value})], (_e0))} placeholder={`Auditor Login`} type={`text`}/>
  <Input onBlur={(_e0) => addEvents([Event("state.set_email", {value:_e0.target.value})], (_e0))} placeholder={`link to ticket`} type={`text`}/>
  <Select onChange={(_e0) => addEvents([Event("state.set_floor", {value:_e0.target.value})], (_e0))} placeholder={`Select Floor`}>
  <option value={`A01`}>
  {`A01`}
</option>
  <option value={`A02`}>
  {`A02`}
</option>
  <option value={`A03`}>
  {`A03`}
</option>
  <option value={`A04`}>
  {`A04`}
</option>
</Select>
  <Select onChange={(_e0) => addEvents([Event("state.set_job", {value:_e0.target.value})], (_e0))} placeholder={`Station Type`}>
  <option value={`Arsaw`}>
  {`Arsaw`}
</option>
  <option value={`Universal`}>
  {`Universal`}
</option>
</Select>
  <Input onBlur={(_e0) => addEvents([Event("state.set_location", {value:_e0.target.value})], (_e0))} placeholder={`Station #`} type={`text`}/>
  <Select onChange={(_e0) => addEvents([Event("state.set_gender", {value:_e0.target.value})], (_e0))} placeholder={`Select Reason`}>
  <option value={`Computer Screen`}>
  {`Computer Screen`}
</option>
  <option value={`FC Games`}>
  {`FC Games`}
</option>
  <option value={`Scanner`}>
  {`Scanner`}
</option>
  <option value={`IDS`}>
  {`IDS`}
</option>
  <option value={`Bin Filter`}>
  {`Bin Filter`}
</option>
  <option value={`Fan`}>
  {`Fan`}
</option>
  <option value={`Mat`}>
  {`Mat`}
</option>
  <option value={`Safety Tape`}>
  {`Safety Tape`}
</option>
  <option value={`Rack Light`}>
  {`Rack Light`}
</option>
  <option value={`Arsaw Gate`}>
  {`Arsaw Gate`}
</option>
  <option value={`Broom`}>
  {`Broom`}
</option>
</Select>
  <ButtonGroup isAttached={false} spacing={30}>
  <Tooltip label={` 💡 Please verify you've entered all data correctly before submitting 💡`} shouldWrapChildren={true}>
  <Button onClick={(_e) => addEvents([Event("state.add_customer", {})], (_e))}>
  {`Submit`}
</Button>
</Tooltip>
  <Button onClick={(_e) => addEvents([Event("state.customer_page", {})], (_e))}>
  <ArrowBackIcon/>
</Button>
</ButtonGroup>
</VStack>
</Center>
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
