const { chromium } = require("playwright");

async function capturePinterestResetRequest(browser, email, password = null) {
    if (password === null) {
        password = email;
    }

    const context = await browser.newContext({
        locale: "de-DE"
    });

    const page = await context.newPage();

    const captured = {};

    page.on("request", request => {
        if (request.url().includes("UserSessionResource/create")) {
            captured.url = request.url();
            captured.headers = request.headers();
            captured.post = request.postData();
        }
    });


    async function checkUIErrors() {
        while (true) {
            const alert = page.locator('[role="alert"]');

            if (await alert.isVisible().catch(() => false)) {
                captured.alerts = await alert.allInnerTexts();
                return;
            }

            await page.waitForTimeout(100);
        }
    }

    const errorTask = checkUIErrors();


    try {
        // Load page
        await page.goto(
            "https://de.pinterest.com/",
            {
                waitUntil: "domcontentloaded"
            }
        );


        // Decline cookies if banner appears
        const cookieDecline = page.locator(
            'button:has-text("Alle ablehnen")'
        );

        try {
            await cookieDecline.waitFor({
                state: "visible",
                timeout: 5000
            });

            await cookieDecline.click({
                force: true
            });

        } catch (e) {
            // cookie banner not shown
        }


        const loginModal = page.locator(
            '[data-test-id="login-modal-default"]'
        );


        // Open login if needed
        if (!await loginModal.isVisible().catch(() => false)) {

            const loginButton = page.locator(
                '[data-test-id="simple-login-button"]'
            );

            await loginButton.waitFor({
                state: "visible",
                timeout: 15000
            });

            await loginButton.click({
                force: true
            });
        }


        // Wait for login fields
        await loginModal.waitFor({
            state: "visible",
            timeout: 15000
        });


        const emailInput = page.locator(
            '[data-test-id="emailInputField"]'
        );

        const passwordInput = page.locator(
            '[data-test-id="passwordInputField"]'
        );


        await emailInput.waitFor({
            state: "visible"
        });

        await passwordInput.waitFor({
            state: "visible"
        });


        await emailInput.fill(email);
        await passwordInput.fill(password);


        // Check captcha
        const captcha = page.locator(
            "iframe[src*='captcha'], [data-captcha], .captcha"
        );

        if (await captcha.isVisible().catch(() => false)) {
            return {
                alerts: [
                    "Captcha detected"
                ]
            };
        }


        const submit = page.locator(
            '[data-test-id="registerFormSubmitButton"] button'
        );


        await submit.waitFor({
            state: "visible"
        });


        // Wait until clickable
        while (!await submit.isEnabled()) {
            await page.waitForTimeout(100);
        }


        await submit.click();


        // Wait until alert appears or timeout
        await Promise.race([
            errorTask,
            new Promise(resolve => setTimeout(resolve, 15000))
        ]);


        // If watcher didn't catch it, check manually
        if (!captured.alerts) {
            captured.alerts = await page.locator(
                '[role="alert"]'
            ).allInnerTexts();
        }


        return {
            alerts: captured.alerts
        };


    } finally {
        await context.close();
    }
}

