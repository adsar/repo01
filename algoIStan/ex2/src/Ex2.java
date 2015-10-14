import java.io.*;
import java.util.*;

public class Ex2 {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {	
		
		ArrayList<Integer> al = readArray("QuickSort.txt");
		Integer a[] = al.toArray(new Integer[al.size()]);
		QuickSort quickSort = new QuickSort();
		
		long numComparisons1 = quickSort.Sort(a, 0, al.size(), new Selector1());

		// reassign, or the number of comps will change, also, because in a sorted array the performance is n**2
		a = al.toArray(new Integer[al.size()]);
		long numComparisons2 = quickSort.Sort(a, 0, al.size(), new Selector2());
		//long numComparisons2 = 0;

		// read again, or the number of comps will change
		a = al.toArray(new Integer[al.size()]);	
		long numComparisons3 = quickSort.Sort(a, 0,  al.size(), new Selector3());
		
		System.out.println(String.format("%d %d %d", numComparisons1, numComparisons2, numComparisons3));
	}
	
	public static ArrayList<Integer> readArray(String path) throws IOException {
		ArrayList<Integer> arr = new ArrayList<Integer>();
		BufferedReader br = new BufferedReader(new FileReader(path));
	    try {
	        String line = br.readLine();
	        while (line != null) {
		        arr.add(Integer.parseInt(line));
		        line = br.readLine();
		    }
		} finally {
		    br.close();
		}
	    return arr;
	}
}
