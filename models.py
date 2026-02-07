"""
Object-Oriented Data Models for Sales Analytics Platform
Demonstrates: OOP, inheritance, polymorphism, and design patterns
"""


class Entity:
    """Base class for all domain entities"""
    
    def __init__(self, id, name):
        """
        Args:
            id: Unique identifier
            name: Entity name
        """
        if not id or not name:
            raise ValueError("id and name cannot be empty")
        self.id = id
        self.name = name
    
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return self.__str__()


class SalesItem(Entity):
    """
    Base class for items sold in the system.
    Demonstrates inheritance: Product and Service both inherit from this.
    """
    
    def __init__(self, id, name, category, base_price):
        """
        Args:
            id: Item ID
            name: Item name
            category: Item category
            base_price: Base price as float
        """
        super().__init__(id, name)
        if base_price < 0:
            raise ValueError("base_price cannot be negative")
        self.category = category
        self.base_price = base_price
    
    def get_price(self, quantity: int = 1) -> float:
        """
        Get price for quantity. Overridden in subclasses.
        Demonstrates polymorphism: subclasses override this method.
        """
        return self.base_price * quantity
    
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, category={self.category}, price=${self.base_price})"


class Product(SalesItem):
    """
    Represents a physical product.
    Inherits from SalesItem. Simple pricing model.
    """
    
    def __init__(self, id, name, category, base_price, stock_quantity: int = 0):
        """
        Args:
            id: Product ID
            name: Product name
            category: Product category
            base_price: Base price per unit
            stock_quantity: Current stock level
        """
        super().__init__(id, name, category, base_price)
        if stock_quantity < 0:
            raise ValueError("stock_quantity cannot be negative")
        self.stock_quantity = stock_quantity
    
    def get_price(self, quantity: int = 1) -> float:
        """Product pricing: simple per-unit cost"""
        if quantity < 0:
            raise ValueError("quantity cannot be negative")
        return self.base_price * quantity
    
    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, category={self.category}, price=${self.base_price}, stock={self.stock_quantity})"


class Service(SalesItem):
    """
    Represents a service (not physical).
    Inherits from SalesItem. Different pricing model (hourly rate).
    
    Demonstrates polymorphism: overrides get_price() differently than Product.
    """
    
    def __init__(self, id, name, category, hourly_rate: float, duration_hours: float = 1.0):
        """
        Args:
            id: Service ID
            name: Service name
            category: Service category
            hourly_rate: Price per hour
            duration_hours: Default duration in hours
        """
        super().__init__(id, name, category, hourly_rate)
        if duration_hours <= 0:
            raise ValueError("duration_hours must be positive")
        self.duration_hours = duration_hours
    
    def get_price(self, quantity: int = 1) -> float:
        """
        Service pricing: hourly_rate * duration_hours * quantity
        Shows different calculation than Product.get_price()
        """
        return self.base_price * self.duration_hours * quantity
    
    def __str__(self):
        return f"Service(id={self.id}, name={self.name}, category={self.category}, hourly_rate=${self.base_price}, duration={self.duration_hours}h)"


class Customer(Entity):
    """
    Base Customer class.
    Demonstrates inheritance hierarchy: RegularCustomer, PremiumCustomer, CorporateCustomer.
    """
    
    def __init__(self, id, name, email, lifetime_value=0.0):
        """
        Args:
            id: Customer ID
            name: Customer name
            email: Email address
            lifetime_value: Total value of all purchases
        """
        super().__init__(id, name)
        if "@" not in email:
            raise ValueError("Invalid email format")
        self.email = email
        self.lifetime_value = lifetime_value
    
    def get_discount_rate(self) -> float:
        """
        Get discount rate based on customer tier.
        Overridden in subclasses. Demonstrates polymorphism.
        """
        return 0.0  # Base customer: no discount
    
    def apply_discount(self, amount: float) -> float:
        """Apply customer-specific discount to order amount"""
        discount_rate = self.get_discount_rate()
        return amount * (1 - discount_rate)
    
    def __str__(self):
        return f"Customer(id={self.id}, name={self.name}, email={self.email}, ltv=${self.lifetime_value:,.2f})"


class RegularCustomer(Customer):
    """Regular customer tier: No special discount"""
    
    def get_discount_rate(self) -> float:
        """Regular customers: 0% discount"""
        return 0.0
    
    def __str__(self):
        return f"RegularCustomer(id={self.id}, name={self.name}, ltv=${self.lifetime_value:,.2f}, discount=0%)"


class PremiumCustomer(Customer):
    """
    Premium customer tier: Loyalty-based discount.
    Demonstrates polymorphism: different discount logic.
    """
    
    def __init__(self, id, name, email, lifetime_value=0.0, years_member: int = 1):
        """
        Args:
            id: Customer ID
            name: Customer name
            email: Email address
            lifetime_value: Total value of purchases
            years_member: Years as premium member
        """
        super().__init__(id, name, email, lifetime_value)
        if years_member < 1:
            raise ValueError("years_member must be at least 1")
        self.years_member = years_member
    
    def get_discount_rate(self) -> float:
        """
        Premium customers: 5% base + 1% per year of membership.
        Up to maximum 15% discount.
        """
        base_discount = 0.05
        loyalty_bonus = min(0.01 * self.years_member, 0.10)  # Max 10% loyalty bonus
        return min(base_discount + loyalty_bonus, 0.15)  # Cap at 15%
    
    def __str__(self):
        discount_pct = self.get_discount_rate() * 100
        return f"PremiumCustomer(id={self.id}, name={self.name}, ltv=${self.lifetime_value:,.2f}, discount={discount_pct:.1f}%, years={self.years_member})"


class CorporateCustomer(Customer):
    """
    Corporate/Bulk customer tier: Volume-based discount.
    Demonstrates different discount calculation strategy.
    """
    
    def __init__(self, id, name, email, lifetime_value=0.0, company_name: str = "", annual_volume: float = 0.0):
        """
        Args:
            id: Customer ID
            name: Contact name
            email: Email address
            lifetime_value: Total value of purchases
            company_name: Name of the company
            annual_volume: Annual purchase volume
        """
        super().__init__(id, name, email, lifetime_value)
        self.company_name = company_name or name
        if annual_volume < 0:
            raise ValueError("annual_volume cannot be negative")
        self.annual_volume = annual_volume
    
    def get_discount_rate(self) -> float:
        """
        Corporate customers: Volume-based discount.
        $0-10k: 5%, $10-50k: 10%, $50k+: 15%
        """
        if self.annual_volume >= 50000:
            return 0.15
        elif self.annual_volume >= 10000:
            return 0.10
        else:
            return 0.05
    
    def __str__(self):
        discount_pct = self.get_discount_rate() * 100
        return f"CorporateCustomer(id={self.id}, company={self.company_name}, ltv=${self.lifetime_value:,.2f}, discount={discount_pct:.1f}%, volume=${self.annual_volume:,.0f})"


class Order(Entity):
    """Represents a sales order"""
    
    VALID_STATUSES = {"completed", "cancelled", "pending"}
    
    def __init__(self, id, date, customer_id, amount, status="pending"):
        """
        Args:
            id: Order ID
            date: Order date (datetime object)
            customer_id: Associated customer ID
            amount: Order amount as float
            status: Order status (completed, cancelled, pending)
        """
        super().__init__(id, f"Order {id}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        
        self.date = date
        self.customer_id = customer_id
        self.amount = amount
        self.status = status
    
    def __str__(self):
        return f"Order(id={self.id}, date={self.date}, customer_id={self.customer_id}, amount={self.amount}, status={self.status})"
