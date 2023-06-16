""" Contains the Range class, which stores the bounds of a cluster and allows
operations to be performed between them."""

from typing import Optional
import datetime as dt # NEW

class Range():

    """Stores the lower and upper values for a cluster on a single axis. """

    def __init__(self, lower: Optional[float] = None, upper: Optional[float] = None):
        """Initialises the Range with given lower and upper values, or 0s if not provided

        Kwargs:
            lower (float): The lower bound of the Range
            upper (float): The upper bound of the Range

        """
        # not a nice solution, date strings have len 10 and time strings have len 8
        #if( isinstance(lower, str) & isinstance(upper, str) ):
        #    if ( (len(lower) == 10) & (len(upper) == 10)): # NEW
        #        lower = dt.datetime.strptime(lower, '%Y-%m-%d').date() # NEW
        #        upper = dt.datetime.strptime(upper, '%Y-%m-%d').date() # NEW
        #    
        #    elif( (len(lower) == 8) & (len(upper) == 8) ): # NEW
        #        lower = dt.datetime.strptime(lower, '%H:%M:%S').time() # NEW
        #        upper = dt.datetime.strptime(upper, '%H:%M:%S').time() # NEW
                
        self.lower = lower
        self.upper = upper

    def update(self, value: float):
        """Updates the range if the given value does not fit within the current
        bounds

        Args:
            value (float): A new value to bounds check and update the Range
            with if needed

        """

        self.lower = min(self.lower, value) if self.lower is not None else value
        self.upper = max(self.upper, value) if self.upper is not None else value

    def information_loss(self, other) -> float:
        """Calculates VInfoLoss of other defined on Page 4 of the CASTLE paper

        Args:
            other (Range): Global range of this attribute

        Returns: VInfoLoss with respect to other

        """
        diff_self = self.difference()
        diff_other = other.difference()

        if(isinstance(diff_other, dt.timedelta)):
           if((diff_other.days == 0) | (diff_other.seconds == 0)):
               return 0
        # Deal with division by 0
        if (diff_other == 0):
            return 0

        return diff_self / diff_other

    def within_bounds(self, value: float):
        """Checks whether the value is within the bounds of the range.

        Args:
            value: The value to perform bounds checking for

        Returns: Whether or not the value is in bounds

        """
        return self.lower <= value <= self.upper

    def difference(self):
        """Finds the total range of this item

        Args:
            value: The value to perform bounds checking for

        Returns: Difference between upper and lower

        """
        #if( isinstance(self.lower, str) & isinstance(self.upper, str) ):
        #    if ( (len(self.lower) == 10) & (len(self.upper) == 10)): # NEW
        #        self.lower = dt.datetime.strptime(self.lower, '%Y-%m-%d').date() # NEW
        #        self.upper = dt.datetime.strptime(self.upper, '%Y-%m-%d').date() # NEW
        #    
        #    elif( (len(self.lower) == 8) & (len(self.upper) == 8) ): # NEW
        #        self.lower = dt.datetime.strptime(self.lower , '%H:%M:%S')#.time() # NEW
        #        self.upper = dt.datetime.strptime(self.upper , '%H:%M:%S')#.time() # NEW
        ### NEW ### handle time stamps
        if(isinstance(self.lower, dt.time) & isinstance(self.upper, dt.time)):
            low_delta = dt.timedelta(hours = self.lower.hour, minutes = self.lower.minute, seconds = self.lower.second)
            up_delta = dt.timedelta(hours = self.upper.hour, minutes = self.upper.minute, seconds = self.upper.second)
            dif = up_delta - low_delta
            return dif #.seconds
        
        ### NEW ### handle dates
        elif(isinstance(self.lower, dt.date) & isinstance(self.upper, dt.date)):
            dif = self.upper - self.lower
            return dif #.days
        
        else:
            return abs(self.upper - self.lower)

    def __truediv__(self, other):
        """Allows for the shorthand notation r1/r2 instead of r1.information_loss(r2)

        Args:
            other: The other range to use

        Returns: The information_loss of other

        """
        return self.information_loss(other)

    def __str__(self):
        """Creates a string representation of the current Range
        Returns: A string representation of the current Range

        """
        return "Range [{}, {}]".format(self.lower, self.upper)
