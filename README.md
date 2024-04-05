# Sample Trading Algorithm For RIT

This is a very rudimentary implementation of a trading algorithm for RIT and uses the RIT Client API documented
at https://rit.306w.ca/RIT-REST-API-DEV/1.0.3/.

## Setup

1. Start PyCharm Community Edition.

   a. Click **Get from VCS**.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/5e66734b-4b86-4f63-9638-6a26270ca592)

   b. Use this repository as the **URL**.
      ```
      https://github.com/306W/rit-market-maker-python
      ```

   c. Click **Clone**.

   d. If prompted to select an interpreter, click **Cancel** on the dialog (we will be using the the Project Settings
   window to setup the interpreter).

   e. Open the Project Settings window (hamburger menu on the top left) > **Settings...**, then in the tree navigation
   on the left, go to **Project: <name of project>** > **Python Interpreter**.
    - Click **Add Interpreter** > **Add Local Interpreter...**
    - In the tree navigation, select **Conda Environment**.
    - Ensure **Use existing environment** is selected.

      ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/077845e2-39fd-4055-9f44-b1e8c43baf26)

    - Click **OK** and **OK** again to return to the main window.

   f. Open up the built-in terminal.

      ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/99f40612-55d8-4f59-b5a8-902321bd2931)

   g. Install the dependencies in `requirements.txt`.

      ```bash
      pip install -r requirements.txt
      ```

2. Open **RIT 2.0 Client** and login with your credentials.

3. Update the `settings.py` file with the API key / port found in the API Info window in the RIT client. If the API is showing an error, it means that somebody else is using that port (the VM instances are multi-tenant) so change it to a different random port and ensure the settings file matches.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/f9a950de-4d8d-4cf4-be52-c25d14409651)

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/82d242d6-c904-4a8e-8d19-8a3a1081a573)

4. Run the bot by opening the terminal and running `main.py`.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/b0b84a37-a128-4677-a08e-89f186eb2103)

   ```bash
   python main.py
   ```
