from fastapi import HTTPException, status
from app.models.cart import Cart, CartItem, CartStatus
from app.models.actor import Actor
from app.repositories.abstract_cart_repository import AbstractCartRepository
from typing import Optional

class CartService:
    def __init__(self, repository: AbstractCartRepository):
        self.repo = repository

    async def get_or_create_active_cart(self, actor: Actor) -> Cart:
        if not self.actor.is_buyer():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only buyers can create and manage carts"
            )
        
        try:
            cart = await self.repo.get_user_active_cart(self.actor.id)
            if not cart:
                cart = await self.repo.create_cart(self.actor.id)
            return cart
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get or create cart: {str(e)}"
            )

    async def add_item(self, item: CartItem, actor: Actor) -> Cart:
        try:
            cart = await self.get_or_create_active_cart(actor)
            self._validate_ownership(cart, actor)
            
            # Заглушка для интеграции с Product Catalog
            
            existing_product_ids = {item.product_id for item in cart.items}
            if len(existing_product_ids) >= 100 and item.product_id not in existing_product_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cart cannot contain more than 100 different products"
                )
            
            updated_cart = cart.add_item(item)
            await self.repo.save_cart(updated_cart)
            return updated_cart
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add item to cart: {str(e)}"
            )

    async def remove_item(self, product_id: str) -> Cart:
        try:
            cart = await self.get_or_create_active_cart()
            self._validate_ownership(cart)
            
            updated_cart = cart.remove_item(product_id)
            await self.repo.save_cart(updated_cart)
            return updated_cart
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove item from cart: {str(e)}"
            )

    async def clear_cart(self) -> Cart:
        try:
            cart = await self.get_or_create_active_cart()
            self._validate_ownership(cart)
            
            updated_cart = cart.clear()
            await self.repo.save_cart(updated_cart)
            return updated_cart
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to clear cart: {str(e)}"
            )
    
    async def convert_cart_to_order(self, cart_id: str) -> None:
        try:
            cart = await self.repo.get_cart(cart_id)
            if not cart:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart not found"
                )
            
            self._validate_ownership(cart)
            cart.mark_as_converted()
            await self.repo.save_cart(cart)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to convert cart to order: {str(e)}"
            )

    def _validate_ownership(self, cart: Cart, actor: Actor):
        if cart.user_id != self.actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this cart"
            )