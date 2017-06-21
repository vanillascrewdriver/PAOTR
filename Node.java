package edu.umd.BG.PAOTR;
import java.util.*;
import edu.umd.BG.PAOTR.*;
public class Node {
	private List<Node> children;
	private List<Leaf> leafs;
	private Node parent;
	private String name;
	private String function;
	public Node(String name, String function, List<Node> children, List<Leaf> leafs, Node parent){
		this.name=name;
		this.function= function;
		this.children= children;
		this.leafs= leafs;
		this.parent= parent;

	}

	public String getName(){
		return name;
	}

	public String getFunction(){
		return function;
	}

	public List<Node> getChildren(){
		return children;
	}

	public List<Leaf> getLeafs(){
		return leafs;
	}

	public Node getParent(){
		return parent;
	}

	public void setParent(Node parent){
		this.parent=parent;
	}

	public void addChild(String name, String function, List<Node> children, List<Leaf> leafs, Node parent){
		this.children.add(new Node(name, function, children, leafs, parent=this));
	}

	public void addChildNode(Node node){
		this.children.add(node);
	}

	public void addLeaf(String name, double probability, double cost){
		this.leafs.add(new Leaf(name, probability, cost, null));
	}

	public void addLeaf(String name, double probability, double cost, Node parent){
		this.leafs.add(new Leaf(name, probability, cost, parent));
	}

	public void addLeafNode(Leaf leaf){
		this.leafs.add(leaf);
	}

	public void sortLeafs(){
		Leaf[] leafy= new Leaf[1];
		Leaf[] leafy1= this.leafs.toArray(leafy);
		double[] Rratio= new double[leafy.length];

		for(int i=0; i<leafy1.length; i++){
			Rratio[i]= leafy1[i].getRatio();
		}

		Arrays.sort(Rratio);
		List<Leaf> reverse= new ArrayList<Leaf>();
		for(int i=Rratio.length-1; i>=0; i--){
			Leaf leafy2= new Leaf();//Should have default constructor but what is the default values?
			for(int j=0; j<leafy.length; j++){
				if(leafy[j].getRatio()==Rratio[i]){
					leafy2=leafy[j];
				}
			}
			reverse.add(leafy2);
		}
		this.leafs=reverse;
	}

	public boolean isDescendent(Node descendant){
		for (int i=0; i<this.getChildren().size(); i++){
			if(descendant==this.getChildren().get(i)){
				return true;
			}
		}

		for (int i=0; i<this.getChildren().size(); i++){
			if(this.getChildren().get(i).isDescendent(descendant)){
				return true;
			}
		}

		return false;
	}

	public Node removeChild(Node child){
		return this.children.remove(this.children.indexOf(child));
	}

	public Leaf removeLeaf(Leaf leaf){
		return this.leafs.remove(this.leafs.indexOf(leaf));
	}


	public List<Double> getLeafProbabilities(){
		List<Double> probs= new ArrayList<Double>();

		if(this.getFunction()=="and"){
			for(Leaf leaf: this.getLeafs()){
				probs.add(leaf.getProbability());		
			}

		}
		else{
			for(Leaf leaf: this.getLeafs()){
				probs.add(1-leaf.getProbability());
			}
		}
		return probs;
	}

	public Double getProbability(){
		List<Double> probsMul= this.getLeafProbabilities();
		Double probsMulti=probsMul.get(0);
		for(int i=1; i<probsMul.size(); i++){
			probsMulti*=probsMul.get(i);
		}

		if(this.getFunction()=="and"){
			return probsMulti;
		}

		else{
			return 1-probsMulti;
		}
	}

	public Double getCostN(){
		List<Double> probs= this.getLeafProbabilities();
		List<Double> costs= new ArrayList<Double>();
		double g=0;
		double cost=0;
		for(int i=0; i< this.getLeafs().size(); i++){
			costs.add(this.getLeafs().get(i).getCost());
		}

		for(int i=0; i<costs.size(); i++){
			for(int j=0; j<i; j++){
				g*= probs.get(j);
			}

			cost+=costs.get(i)*g;
			g=0;
		}
		return cost;
	}
}