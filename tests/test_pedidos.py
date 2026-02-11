import pytest
from models.pedido import Pedido

class Test_Pedidos:

    def test_obtenerPedidos(self):
        """
        Verifica que se obtengan pedidos
        """
        pedido = Pedido()
        result = pedido.obtenerPedidos()
        assert isinstance(result, list)
        assert len(result) >= 0

    def test_buscar_pedido_existente(self):
        """
        Verifica que un pedido existente regrese datos
        """
        pedido = Pedido()
        resultado = pedido.buscarPedido(6)
        assert resultado is not None
        assert resultado["id"] == 6


    def test_buscar_pedido_inexistente(self):
        """
        Verifica que un pedido inexistente regrese None
        """
        pedido = Pedido()
        resultado = pedido.buscarPedido(9999)
        assert resultado is None