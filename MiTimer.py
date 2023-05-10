from threading import Timer

class MiTimer( Timer ):
    def __init__( self, interval, function, args=[], kwargs={} ):
        self._original_function = function
        super( MiTimer, self ).__init__( interval, self._do_execute, args, kwargs )
    def _do_execute( self, *a, **kw ):
        self.result = self._original_function( *a, **kw )

    def join( self ):
        super( MiTimer, self ).join()
        return self.result
