"""
List of base categories for the application
"""

from src.models import Category

GENERAL = Category(id="k2Bnio4r4rumjEtf7KAnRP", title="General", icon="rectangle-stack", color="#FFD700")
TRANSPORT = Category(id="nmvY3NerXM3t8n3GCD3S9e", title="Transport", icon="truck", color="#FF4500")
HOUSING = Category(id="8dbxskvYv3k672TJCjniQx", title="Housing", icon="home", color="#FF6347")
GROCERIES = Category(id="anXz4uDvzF29jzUqX7cyPq", title="Groceries", icon="shopping-cart", color="#228B22")
SHOPPING = Category(id="3v2znBBbuK6aDTAkRdfsB6", title="Shopping", icon="shopping-bag", color="#0000FF")
BILLS = Category(id="TETAxd9u4he5dCWXZbBpRh", title="Bills", icon="credit-card", color="#FF0000")
ENTERTAINMENT = Category(id="TZuwyBFHemk95U6avZfvEf", title="Entertainment", icon="film", color="#8A2BE2")
EATING_OUT = Category(id="TdTY9ahjNKanyAvyUCmUth", title="Eating Out", icon="cake", color="#FF1493")
CHARITY = Category(id="AXLpno5SHNDB2WXvQSdzCZ", title="Charity", icon="gift", color="#FF00FF")
PERSONAL_CARE = Category(id="nK9LfGwKsFpv87XY8FYLY2", title="Personal Care", icon="heart", color="#FF69B4")
BUSINESS = Category(id="8GshVk2jfcs4BKnLTVzx2w", title="Business", icon="briefcase", color="#D2691E")
FAMILY = Category(id="WAP4XhPHr3tSX6Rc696hf4", title="Family", icon="user-group", color="#B0E0E6")
EDUCATION = Category(id="Q3enGA7mRz3zGE59edkhBB", title="Education", icon="academic-cap", color="#4682B4")
INVESTMENTS = Category(id="YdkFskyaobeDR4dVmFqUv9", title="Investments", icon="chart-bar", color="#FFD700")
HOLIDAYS = Category(id="Liwwdaqt7fPJ6LKFACjpiX", title="Holidays", icon="calendar", color="#FF4500")
CASH = Category(id="RDrzJ8BzASa6yNgecSPSfF", title="Cash", icon="currency-pound", color="#FF6347")
INCOME = Category(id="jHC68t25b7qtqkUQq4Ny3C", title="Income", icon="currency-dollar", color="#228B22")
EXCLUDED = Category(id="djwbVbfUrL2K5xFVutSq2v", title="Excluded", icon="eye-slash", color="#0000FF")


"""
Base mapping of categories to keywords
"""

mapping = {
    GENERAL.id: ["General"],
    TRANSPORT.id: ["Transport", "Uber", "Rail Services"],
    HOUSING.id: ["Rent", "Mortgage", "Utilities"],
    GROCERIES.id: ["Tesco", "Supermarket"],
    SHOPPING.id: ["Shopping", "Amazon", "eBay"],
    BILLS.id: ["Bills", "Utilities", "Council Tax"],
    ENTERTAINMENT.id: ["Entertainment", "Netflix", "Spotify"],
    EATING_OUT.id: ["Eating Out", "Restaurants", "Takeaway"],
    CHARITY.id: ["Charity", "Donation"],
    PERSONAL_CARE.id: ["Personal Care", "Pharmacy", "Haircut", "Beauty"],
}