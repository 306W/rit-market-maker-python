# Sample Trading Algorithm For RIT

This is a very rudimentary implementation of a trading algorithm for RIT and uses the RIT Client API documented
at https://rit.306w.ca/RIT-REST-API-DEV/1.0.3/.

## Setup

1. Start PyCharm Community Edition.

   a. Click **Get from VCS**.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/0c3744c4-905e-4339-84a7-47713f419c61)

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

      ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/32220d54-b108-4d6d-8051-806bb95bfed6)

    - Click **OK** and **OK** again to return to the main window.

   f. Open up the built-in terminal.

      ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/a846455f-bd83-4071-897d-86ef482fb60c)

   g. Install the dependencies in `requirements.txt`.

      ```bash
      pip install -r requirements.txt
      ```

2. Open **RIT 2.0 Client** and login with your credentials.

3. Update the `settings.py` file with the API key / port found in the API Info window in the RIT client. If the API is showing an error, it means that somebody else is using that port (the VM instances are multi-tenant) so change it to a different random port and ensure the settings file matches.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/20a1bdcf-0223-4177-ad9d-b778ad7cff78)

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/4e2c6728-263d-4210-967e-e788ae85960a)

4. Run the bot by opening the terminal and running `main.py`.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/381f775b-3566-46e8-884a-2f1a317bdcfd)

   ```bash
   python main.py
   ```

## Development

To extend the trading logic, simply edit `CustomArbitrageBot.py` or alternatively extend the `BaseArbitrageBot` with your own implementation.
