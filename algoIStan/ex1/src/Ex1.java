import java.io.*;
import java.util.*;

public class Ex1 {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {	
		
		ArrayList<Integer> a = readArray("IntegerArray.txt");
		long numInversions = countInversions(a);
		System.out.println(numInversions);
	}
	
	public static long countInversions(ArrayList<Integer> a) {
	
		int n = a.size();
		
		// base case
		if (n == 1) return 0; 
		
		// main case
		int n2 = n / 2;
		ArrayList<Integer> al = new ArrayList<Integer>();
		ArrayList<Integer> ar =  new ArrayList<Integer>();
		for (int i=0; i<n2; i++) al.add(a.get(i));
		for (int i=n2; i<a.size(); i++) ar.add(a.get(i));
		long cl = countInversions(al);
		long cr = countInversions(ar);
		// al and ar will be sorted after the calls above
		
		// merge the two sub-arrays and count split inversions
		// put the resulting sorted array in a (the argument)
		a.clear();
		long count_split = mergeAndCountSplitInversions(al, ar, a);
		
		return cl + cr + count_split;
	}
	
	public static long mergeAndCountSplitInversions(ArrayList<Integer> al, ArrayList<Integer> ar, ArrayList<Integer> m) {
		int i = 0, j = 0;
		long count = 0;
		
		while (true) {
			if (i<al.size() && j<ar.size()) {
				if (al.get(i) < ar.get(j)) {
					m.add(al.get(i));
					i++;
				} else {
					count += (al.size() - i); // count inversions
					m.add(ar.get(j));
					j++;
				}
			} else if (i<al.size()) {
				m.add(al.get(i));
				i++;
			} else if (j<ar.size()) {
				m.add(ar.get(j));
				j++;
			} else break;
		}
		
		return count;
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
