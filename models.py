class Entity:
    """
    Base class for all domain entities.
    """
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

class Product(Entity):
    """
    Base class for products sold in the system.
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

    def __str__(self):
        """
        Override string representation to include category and price.
        """
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, category={self.category}, price=${self.base_price})"

class Customer(Entity):
    """
    Represents a customer in the system.
    """
    def __init__(self, id, name, email, lifetime_value=0.0):
        """
        Args:
            id: Customer ID
            name: Customer name
            email: Customer email
            lifetime_value: Total value of purchases made by the customer
        """
        super().__init__(id, name)
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        self.email = email
        self.lifetime_value = lifetime_value
    
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, lifetime_value={self.lifetime_value})"
    
class Order(Entity):
    """
    Represents an order placed by a customer.
    """
    def __init__(self, id, name, customer_id, product_ids, total_amount, status="pending"):
        """
        Args:
            id: Order ID
            name: Order name
            customer_id: ID of the customer who placed the order
            product_ids: List of product IDs included in the order
            total_amount: Total amount for the order
            status: Current status of the order (completed, cancelled, pending)
        """
        super().__init__(id, name)
        if not customer_id:
            raise ValueError("customer_id cannot be empty")
        if not product_ids or not isinstance(product_ids, list):
            raise ValueError("product_ids must be a non-empty list")
        if total_amount < 0:
            raise ValueError("total_amount cannot be negative")
        
        self.customer_id = customer_id
        self.product_ids = product_ids
        self.total_amount = total_amount
        self.status = status
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, customer_id={self.customer_id}, products={self.product_ids}, total_amount=${self.total_amount}, status={self.status})"