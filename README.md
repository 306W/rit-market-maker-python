# Sample Market Maker For RIT

This is a very rudimentary implementation of a market making bot for RIT and uses the RIT Client API documented
at https://rit.306w.ca/RIT-REST-API-DEV/1.0.3/.

## Setup

1. Start PyCharm Community Edition.

   a. Click **Get from VCS**.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/4a884332-3e91-4366-a080-cd548c24c2b6)

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
    - Ensure **Create new environment** is selected.

      ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/21268538-c872-4bb5-abbb-0b6faf2436e3)

    - Click **OK** and **OK** again to return to the main window.

   f. Open up the built-in terminal.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/d8dff4de-84a6-4742-a54c-adf6a6cc6919)

   g. Install the dependencies in `requirements.txt`.

      ```bash
      pip install -r requirements.txt
      ```

3. Open **RIT 2.0 Client** and login with your credentials.

4. Update the `settings.py` file with the API key / port found in the API Info window in the RIT client.

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/5af4452b-b9c5-4764-82c2-25a3f9086e0b)

   ![image](https://github.com/306W/rit-market-maker-python/assets/2671978/e8bdf2d1-f35a-4a9f-b989-82b438fad43a)

5. Run the bot (or alternatively `ctrl+r` should also work).

   ```bash
   python main.py
   ```

### Development

To extend the market making logic, simply edit `CustomArbitrageBot.py` or alternatively extend the `BaseArbitrageBot`
with
your own implementation.
