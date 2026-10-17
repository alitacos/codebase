async def check_if_continue_button_disabled_and_wait_to_reenable_else_return( page: Page, timeout_ms: int = 5000 ) -> bool:

    button = page.locator( "div[role='button']" ).filter( has_text=re.compile( r"^(Continue|Weiter|Continuar|Continuer|Doorgaan|Fortfahren)$", re.I ) ).first

    try:
        # wait until button exists
        await button.wait_for(state="visible", timeout=timeout_ms)

        # wait until it becomes disabled
        await page.wait_for_function( """ (button) => { return button && button.getAttribute("aria-disabled") === "true"; } """, button, timeout=timeout_ms )

        # wait until it becomes enabled again
        await page.wait_for_function( """ (button) => { return button && button.getAttribute("aria-disabled") !== "true"; } """, button, timeout=timeout_ms )
        return True

    except Exception:
        # button never disabled or never re-enabled
        return False


    async def check_if_progressbar_enabled_and_wait_to_hide_else_return( page: Page=None,selector:str="div[role='progressbar']" , timeout_ms: int = 5000 ) -> bool:
    
        progress = page.locator( selector ).first
        visible = None
        hidden = None
        
        try:
            await progress.wait_for( state="visible", timeout=timeout_ms )
            visible = True
        except Exception:
            visible = False
        try:
            await progress.wait_for( state="hidden", timeout=timeout_ms )
            hidden = True
        except Exception:
            hidden = False
        
    

            
    async def check_if_continue_button_disabled_and_wait_to_reenable_else_return(page:Page=None, selector:str="div[role='button']", timeout:int=5000)->bool:
        button = page.locator(selector).filter(has_text=re.compile(r"^(Continue|Weiter|Continuar|Continuer|Doorgaan|Fortfahren)$", re.I)).first

        if await button.count() == 0:
            return False

        try:
            if await button.get_attribute("aria-disabled") != "true":
                return False

            while await button.get_attribute("aria-disabled") == "true":
                await asyncio.sleep(0.1)

            return True

        except Exception:
            return False


    async def check_if_progressbar_enabled_and_wait_to_hide_else_return(page:Page=None, selector:str="div[role='progressbar']", timeout:int=5000)->bool:
        locator = page.locator(selector).first

        if await locator.count() == 0:
            return False

        try:
            if not await locator.is_visible():
                return False

            while await locator.is_visible():
                await asyncio.sleep(0.1)

            return True

        except Exception:
            return False


    async def open_graphQL_grabber_and_get_info(page:Page=None, element:Locator=None, query:str='')->dict:
        graph = {
            "graphQl": None,
            "redirected": False,
            "ErrorMsg": None,
            "Radio": False,
            "TimeoutError": False,
            "Success": False,
        }

        async with page.expect_response(lambda response: "graphql" in response.url and response.request.method == "POST") as response_info:

            await element.fill("")
            await element.fill(query.strip())
            await element.press("Enter")

            start_time = asyncio.get_running_loop().time()

            while True:

                if (asyncio.get_running_loop().time() - start_time) * 1000 > timeout:
                    graph["TimeoutError"] = True
                    break


                await check_if_continue_button_disabled_and_wait_to_reenable_else_return(page=page, timeout=timeout)

                await check_if_progressbar_enabled_and_wait_to_hide_else_return(page=page, timeout=timeout)


                if not page.url.startswith(base_url):
                    graph["redirected"] = True
                    break


                ErrorMsg = await get_error_message_after_submit_from_facebook_recover_page(page=page, timeout_ms=timeout)

                if ErrorMsg:
                    graph["ErrorMsg"] = ErrorMsg
                    break


                if await check_if_radio_exists(page=page):
                    graph["Radio"] = True
                    break


                await asyncio.sleep(0.1)


            try:
                response = await response_info.value
                graph["graphQl"] = await response.json()
            except Exception:
                graph["TimeoutError"] = True


            graph["Success"] = True if graph["graphQl"] and (graph["redirected"] or graph["ErrorMsg"] or graph["Radio"]) else False

            return graph            

            
    base_url = 'https://www.facebook.com/login/identify'
    input_selector = 'input[type="text"]:not([name="email"]):not([name="pass"]), input[id="_r_3_"][type="text"]:not([name="email"]):not([name="pass"]), input[id="_r_2_"][type="text"]:not([name="email"]):not([name="pass"])'
    #step 1:
    await clear_playwright_browser_data_async(page=page)
    #step :
    await try_goto_link_in_playwright_page_and_get_title(page=page,url=base_url)
    #step 3:
    inp_element =  wait_for_input_to_load_and_become_text_injectable(page=page,selector=input_selector,timeout_ms=timeout )
    #step 4:
    if inp_element and page.url.startswith(base-url) :
        page_title_found = get_key_from_sjs_json_data_script_element_in_playwright_page(page =page,selector='script[type="application/json"][data-sjs]',identifiers=["account_search_title","__bbox",],title_key ='account_search_title',     timeout =timeout) 
        if not page_title_found:
            pass#something is wrong. what to do?? just pass?
        if page_title_found:
            ensure_input_object_is_empty_in_playwright_page_bySelector(page=page, selector=input_selector, timeout=timeout) 
            inp_element = wait_for_input_to_load_and_become_text_injectable(page=page, selector=input_selector, timeout=timeout) 
            if not inp_element:
                pass#something is wrong. what to do?? just pass?
            if inp_element:
                return open_graphQL_grabber_and_get_info(page:Page=page,element =inp_element,  query =query)
    return 'ProcessError:something is wrong'