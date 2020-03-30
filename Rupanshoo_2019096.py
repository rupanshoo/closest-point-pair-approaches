"""
CSE101: Introduction to Programming
Assignment 3

Name        : Rupanshoo Saxena
Roll-no     : 2019096
"""



import math
import random



def dist(p1, p2):
    """
    Find the euclidean distance between two 2-D points

    Args:
        p1: (p1_x, p1_y)  
        p2: (p2_x, p2_y)
    
    Returns:
        Euclidean distance between p1 and p2           
    """
    """using the distance formula [ ((x2-x1)^2 + (y2-y1)^2 )^0.5 ] to find the distance between 
    points p1 and p2 whose coordinates are given in the form of a tupple
	"""
    euc_dist = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5  #using distance formula to find the minimum distance between points
    return euc_dist



def sort_points_by_X(points):
    """
    Sort a list of points by their X coordinate

    Args:
        points: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]    sorted
    
    Returns:
        List of points sorted by X coordinate
    """

    points.sort() #sort by default will sort the points in the list with respect to the first element i.e. the x coordinate
    return points
    



def second(val):  #additional function made to assist Sorting by Y coordinate
	return val[1]

def sort_points_by_Y(points):
    """
    Sort a list of points by their Y coordinate

    Args:
        points: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]
    
    Returns:
        List of points sorted by Y coordinate     
    """

    points.sort(key = second)  #sorts the list wrt to the second element since key has been specified here 
    return  points



def naive_closest_pair(plane):
    """
    Find the closest pair of points in the plane using the brute
    force approach

    Args:
        plane: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]

    Returns:
        Distance between closest pair of points and closest pair 
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]  list
    """
     
    min_dist = math.inf  #assigning min dist to infinity
    
    for i in range(len(plane)):  
        for j in range(len(plane)):
            if i!=j:  #so that the same point is not compared with itself
                temp_dist = dist(plane[i],plane[j]) #stores temporary distance
                if temp_dist < min_dist:  #comparing each new distance
                    min_dist = temp_dist  #updating minimum distance
                    small = [min_dist,plane[i],plane[j]]  #small: list that stores minimum distance and the points whose minimum distance is stored 

    return small



def closest_pair_in_strip(points, d): 
    """
    Find the closest pair of points in the given strip with a 
    given upper bound. This function is called by 
    efficient_closest_pair_routine

    Args:
        points: List of points in the strip of interest.
        d: Minimum distance already found found by 
            efficient_closest_pair_routine

    Returns:
        Distance between closest pair of points and closest pair 
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)] if
        distance between p1 and p2 is less than d. Otherwise
        return -1.
    """
    finalreturn = -1  
    n = len(points) #stores no. of points
    points = sort_points_by_Y(points)  #points are stored in order of y-coordinate 
    for i in range(len(points)): 
        for j in range(i+1,min(i+6,n)): #to compare it with the next 5 neighbouring points, n also considered for if there n<5 i.e no. of neighbours is less than 5
            if(dist(points[i],points[j]) < d):  
                d = dist(points[i],points[j]) #stores distance if new distance is lesser than the earlier value which has been passed to the function
                finalreturn = [d,points[i],points[j]]  
    
    return finalreturn                




def efficient_closest_pair_routine(points):  
    """
    This routine calls itself recursivly to find the closest pair of
    points in the plane. 

    Args:
        points: List of points sorted by X coordinate

    Returns:
        Distance between closest pair of points and closest pair 
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """
    if len(points) == 2:  #base case (1) : for 2 points in the strip
        return [dist(points[0],points[1]),points[0],points[1]]
    elif len(points) == 1:  #base case (2) : for a single point in the strip
        return [float("inf")]
    else:
        n=len(points)
        mid = n//2  #stores mid point index
        start = points[:mid]  #first division of the strip
        end = points[mid:]  #second division of the strip
        recur1 = efficient_closest_pair_routine(start) #recursion 1: to divide strip 1 ie the starting strip into further strips till base case is achieved
        recur2 = efficient_closest_pair_routine(end)  #recursion 2 : to divide strip 2 i.e. the ending strip into further strips til base case is achieved
        d = min(recur1[0],recur2[0]) #stores min of the distances between the two strip divisions

        for i in points:
            if(abs(i[0]-points[mid][0])>d): #abs taken so as to compare on either side of the line i.e. the left and the right side and not take the two cases seperately
                points.remove(i) #removes all the points stored in the list which are at a distance greater than d to the line
    
        if(d == recur1[0]): #when minimum distance has been obtained from the first part of the divided strip i.e. start
            tempans = recur1
        else:
            tempans = recur2  #minimum distance from end strip
        
        eff = closest_pair_in_strip(points,d)  

        if eff == -1:  #when d actually stored minimum answer, eff gets -1
            return tempans 
        else:  #updated eff with the updated minimum value gets updated and returned
            return eff
        


def efficient_closest_pair(points):  
    """
    Find the closest pair of points in the plane using the divide
    and conquer approach by calling efficient_closest_pair_routine.

    Args:
        plane: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]

    Returns:
        Distance between closest pair of points and closest pair 
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """

    point_sort = sort_points_by_X(points)  #sorts points with respect to x coordinate
    temp = efficient_closest_pair_routine(point_sort) 
    return temp
    


def generate_plane(plane_size, num_pts):
    """
    Function to generate random points.

    Args:
        plane_size: Size of plane (X_max, Y_max)
        num_pts: Number of points to generate

    Returns:
        List of random points: [(p1_x, p1_y), (p2_x, p2_y), ...]
    """
    
    gen = random.sample(range(plane_size[0]*plane_size[1]), num_pts)
    random_points = [(i%plane_size[0] + 1, i//plane_size[1] + 1) for i in gen]

    return random_points



if __name__ == "__main__":  
    #number of points to generate
    num_pts = 10
    #size of plane for generation of points
    plane_size = (10, 10) 
    plane = generate_plane(plane_size, num_pts)
    print(plane)
    print(naive_closest_pair(plane))
    print(efficient_closest_pair(plane))

