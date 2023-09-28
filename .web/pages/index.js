import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import "gridjs/dist/theme/mermaid.css"
import { Box, Button, Divider, Heading, HStack, Image, Link, Menu, MenuButton, MenuDivider, MenuItem, MenuList, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Stat, StatArrow, StatHelpText, StatLabel, StatNumber, Table, TableContainer, Tbody, Td, Text, Th, Thead, Tooltip, Tr, useColorMode, VStack } from "@chakra-ui/react"
import NextLink from "next/link"
import { AddIcon, EmailIcon, HamburgerIcon, MoonIcon, SunIcon } from "@chakra-ui/icons"
import { Grid as DataTableGrid } from "gridjs-react"
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
  <VStack alignItems={`center`} sx={{"width": "100%"}}>
  <Box sx={{"position": "flex", "width": "100%", "top": "0px", "zIndex": "500"}}>
  <HStack justify={`space-between`} sx={{"borderBottom": "0.2em", "paddingX": "2em", "paddingY": "1em"}}>
  <Tooltip label={`This will open a new tab for creating a ticket.
The Values in the Dahboard are dependent on the data entered 
into Table BELOW, named Trouble Ticket Tracker.
Submitting a ticket alone will not update the Dashboard. 
You must copy link and paste into link field when creating 
a new entry below`} shouldWrapChildren={true}>
  <Link as={NextLink} href={`https://river.amazon.com/?org=fc&buildingId=MIA1`} isExternal={true}>
  <HStack>
  <Image src={`MIA1 concept.png`} sx={{"width": "50px"}}/>
  <Heading size={`lg`} sx={{"fontSize": ["250%", "275%", "300%", "325%", "350%"], "textAlign": "center", "transition": "all 650ms ease"}}>
  {`Create Ticket`}
</Heading>
</HStack>
</Link>
</Tooltip>
  <Box sx={{"width": "25%", "height": "2rem", "display": "flex"}}>
  <Button onClick={toggleColorMode}>
  <Fragment>
  {isTrue((colorMode === "light")) ? (
  <Fragment>
  <SunIcon/>
</Fragment>
) : (
  <Fragment>
  <MoonIcon/>
</Fragment>
)}
</Fragment>
</Button>
</Box>
  <Menu>
  <MenuButton sx={{"bg": "black", "color": "white", "borderRadius": "md", "px": 4, "py": 2}}>
  {`Menu`}
</MenuButton>
  <MenuList>
  <Link as={NextLink} href={`/`}>
  <MenuItem>
  <HStack>
  <Text sx={{"fontSize": ["100%", "115%", "130%", "135%", "125%"], "fontFamily": "Helvectica", "transition": "all 650ms ease", "textAlign": "center"}}>
  {`Home`}
</Text>
  <HamburgerIcon/>
</HStack>
</MenuItem>
</Link>
  <MenuDivider/>
  <Link as={NextLink} href={`/onboarding`}>
  <MenuItem>
  <HStack>
  <Text sx={{"fontSize": ["100%", "115%", "130%", "135%", "125%"], "fontFamily": "Helvectica", "transition": "all 650ms ease", "textAlign": "center"}}>
  {`Audit`}
</Text>
  <AddIcon/>
</HStack>
</MenuItem>
</Link>
</MenuList>
</Menu>
</HStack>
</Box>
  <Box sx={{"position": "flex", "width": "70%", "top": "0px", "zIndex": "500"}}>
  <HStack justify={`space-between`} sx={{"borderBottom": "0.5em", "paddingX": "25em", "paddingY": "1em"}}>
  <Box sx={{"align": "center", "bg": state.statbglogic12, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Overall Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogic12}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic12}`}
  <StatArrow type={`${state.arrowstatlogic12}`}/>
</StatHelpText>
</Stat>
</Box>
</HStack>
  <HStack justify={`space-between`} sx={{"borderBottom": "0.2em", "paddingX": "15em", "paddingY": "1em"}}>
  <Box sx={{"align": "center", "bg": state.statbglogicoverallarsaw, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Overall Arsaw Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicoverallarsaw}
</StatNumber>
  <StatHelpText>
  {`${state.stattextlogicoverallarsaw}`}
  <StatArrow type={`${state.statarrowlogicoverallarsaw}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicoveralluniversal, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Overall Universal Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicoveralluniversal}
</StatNumber>
  <StatHelpText>
  {`${state.stattextlogicoveralluniversal}`}
  <StatArrow type={`${state.statarrowlogicoveralluniversal}`}/>
</StatHelpText>
</Stat>
</Box>
</HStack>
  <HStack justify={`space-between`} sx={{"borderBottom": "0.1em", "paddingX": "2em", "paddingY": "1em"}}>
  <Box sx={{"align": "center", "bg": state.statbglogicA01, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A01 Arsaw Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA01}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA01}`}
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicA02, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A02 Arsaw Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA02}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA02}`}
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicA03, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A03 Arsaw Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA03}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA03}`}
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicA04, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A04 Arsaw Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA04}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA04}`}
</StatHelpText>
</Stat>
</Box>
</HStack>
  <HStack justify={`space-between`} sx={{"borderBottom": ".1em", "paddingX": "2em", "paddingY": "1em"}}>
  <Box sx={{"align": "center", "bg": state.statbglogicA01uni, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A01 Universal Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA01uni}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA01uni}`}
  <StatArrow type={`${state.arrowstatlogicA01uni}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicA02uni, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A02 Universal Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA02uni}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA02uni}`}
  <StatArrow type={`${state.arrowstatlogicA02uni}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicA03uni, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A03 Universal Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA03uni}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA03uni}`}
  <StatArrow type={`${state.arrowstatlogicA03uni}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogicA04uni, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`A04 Universal Readiness`}
</StatLabel>
  <StatNumber>
  {state.statlogicA04uni}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogicA04uni}`}
  <StatArrow type={`${state.arrowstatlogicA04uni}`}/>
</StatHelpText>
</Stat>
</Box>
</HStack>
  <HStack justify={`space-between`} sx={{"borderBottom": "0.1em", "paddingX": "2em", "paddingY": "1em"}}>
  <Box sx={{"align": "center", "bg": state.statbglogic, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Safety Tape`}
</StatLabel>
  <StatNumber>
  {state.statlogic}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic}`}
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic2, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`IDS`}
</StatLabel>
  <StatNumber>
  {state.statlogic2}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic2}`}
  <StatArrow type={`${state.arrowstatlogic2}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic3, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Computer Screen`}
</StatLabel>
  <StatNumber>
  {state.statlogic3}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic3}`}
  <StatArrow type={`${state.arrowstatlogic3}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic4, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`FC Games`}
</StatLabel>
  <StatNumber>
  {state.statlogic4}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic4}`}
  <StatArrow type={`${state.arrowstatlogic4}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic5, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Scanner`}
</StatLabel>
  <StatNumber>
  {state.statlogic5}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic5}`}
  <StatArrow type={`${state.arrowstatlogic5}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic6, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Bin Filter`}
</StatLabel>
  <StatNumber>
  {state.statlogic6}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic6}`}
  <StatArrow type={`${state.arrowstatlogic6}`}/>
</StatHelpText>
</Stat>
</Box>
</HStack>
  <HStack justify={`space-between`} sx={{"borderBottom": "0.2em", "paddingX": "2em", "paddingY": ".2em"}}>
  <Box sx={{"align": "center", "bg": state.statbglogi7, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Fan`}
</StatLabel>
  <StatNumber>
  {state.statlogic7}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic7}`}
  <StatArrow type={`${state.arrowstatlogic7}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic8, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Mat`}
</StatLabel>
  <StatNumber>
  {state.statlogic8}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic8}`}
  <StatArrow type={`${state.arrowstatlogic8}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic9, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Rack Light`}
</StatLabel>
  <StatNumber>
  {state.statlogic9}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic9}`}
  <StatArrow type={`${state.arrowstatlogic9}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic10, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Arsaw Gate`}
</StatLabel>
  <StatNumber>
  {state.statlogic10}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic10}`}
  <StatArrow type={`${state.arrowstatlogic10}`}/>
</StatHelpText>
</Stat>
</Box>
  <Box sx={{"align": "center", "bg": state.statbglogic11, "borderRadius": "md", "width": "100%"}}>
  <Stat>
  <StatLabel>
  {`Broom`}
</StatLabel>
  <StatNumber>
  {state.statlogic11}
</StatNumber>
  <StatHelpText>
  {`${state.stathelptextlogic11}`}
  <StatArrow type={`${state.arrowstatlogic11}`}/>
</StatHelpText>
</Stat>
</Box>
</HStack>
</Box>
  <VStack alignItems={`center`} sx={{"paddingTop": "6em", "width": "70%"}}>
  <Box sx={{"alignItems": "right", "paddingTop": "1em", "display": ["none", "block", "block", "block"]}}>
  <HStack>
  <Heading sx={{"fontSize": ["250%", "275%", "300%", "325%", "350%"], "textAlign": "center", "transition": "all 650ms ease"}}>
  <Text sx={{"backgroundImage": "linear-gradient(271.68deg, #277DA1 0.75%, #43AA8B 88.52%)", "backgroundClip": "text", "fontFamily": "Helvetica", "fontSize": ".9em", "transition": "all 650ms ease", "textAlign": "center"}}>
  {`Trouble Ticket Tracker`}
</Text>
</Heading>
  <Button onClick={(_e) => addEvents([Event("state.onboarding_page", {})], (_e))} sx={{"bg": "linear-gradient(271.68deg, #277DA1 0.75%, #43AA8B 88.52%)", "color": "black", "opacity": "0.8", "_hover": {"opacity": 1}}}>
  {`Create New Entry`}
</Button>
  <Button onClick={(_e) => addEvents([Event("state.webhook", {})], (_e))} sx={{"bg": "linear-gradient(271.68deg, #833AB4 0.75%, #F56040 88.52%)", "color": "black", "opacity": "0.8", "_hover": {"opacity": 1}}}>
  {`Send Slack `}
  <EmailIcon/>
</Button>
</HStack>
  <TableContainer sx={{"bg": " ", "border": "1px solid #ddd", "borderRadius": "5px"}}>
  <Table>
  <Thead>
  <Tr>
  <Th>
  {`Auditor Login`}
</Th>
  <Th>
  {`link to ticket`}
</Th>
  <Th>
  {`Reason`}
</Th>
  <Th>
  {`Floor`}
</Th>
  <Th>
  {`Station #`}
</Th>
  <Th>
  {`Station Type`}
</Th>
  <Th>
  {`Delete`}
</Th>
</Tr>
</Thead>
  <Tbody>
  {state.get_users.map((aqflqajn, i) => (
  <Tr key={i}>
  <Td>
  {aqflqajn.customer_name}
</Td>
  <Td>
  <Link as={NextLink} href={aqflqajn.email} isExternal={true}>
  <Button sx={{"borderRadius": ".3em", "boxShadow": "linear-gradient(271.68deg, #4D908E 0.75%, #43AA8B 88.52%)", "backgroundImage": "linear-gradient(271.68deg, #4D908E 0.75%, #43AA8B 88.52%)", "boxSizing": "border-box", "color": "black", "opacity": "0.8", "_hover": {"opacity": 1}}}>
  {`link to ticket`}
</Button>
</Link>
</Td>
  <Td>
  {aqflqajn.gender}
</Td>
  <Td>
  {aqflqajn.floor}
</Td>
  <Td>
  {aqflqajn.location}
</Td>
  <Td>
  {aqflqajn.job}
</Td>
  <Td>
  <Tooltip label={` ⚠ Before deleting row, please click the "link to ticket" button and verify that the original ticket has been resolved ⚠`} shouldWrapChildren={true}>
  <Button onClick={(_e) => addEvents([Event("state.delete_customer", {email:aqflqajn.email})], (_e))} sx={{"bg": "linear-gradient(#F9844A 0.75%, #E1306C 88.52%)", "color": "black", "opacity": "0.8", "_hover": {"opacity": 1}}}>
  {`Delete`}
</Button>
</Tooltip>
</Td>
</Tr>
))}
</Tbody>
</Table>
</TableContainer>
</Box>
  <DataTableGrid columns={state.dtfr.columns} data={state.dtfr.data} pagination={true} resizable={true} search={true} sort={true}/>
  <Divider/>
</VStack>
</VStack>
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
