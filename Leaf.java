package edu.umd.BG.PAOTR;

import java.util.*;
import edu.umd.BG.PAOTR.*;


public class Leaf {
	private double probability;
	private double cost;
	private Node parent;
	private String name;
	String s="A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z";
	private List<String> names=new ArrayList<String>(Arrays.asList(s.split(",")));;
	public Leaf(String name, double probability, double cost){
		this.name=name;
		this.probability= probability;
		this.cost=cost;
		this.parent=null;

	}

	public Leaf(){
		this.name="";
		this.probability=0.0;
		this.cost=0.0;
		this.parent=null;
	}
	
	public Leaf(String name, double probability, double cost, Node parent){
		this.name=name;
		this.probability= probability;
		this.cost=cost;
		this.parent=parent;
	}

	public String getName(){
		return name;
	}

	public Double getProbability(){
		return probability;
	}
	public Double getCost(){
		return cost;
	}
	public Node getParent(){
		return parent;
	}

	public List<Node> getChildren(){
		List<Node> a= new ArrayList<Node>();
		return a;
	}

	public Double getRatio(){
		if(this.getParent().getFunction()=="or"){
			return this.probability/this.cost;
		}
		else{
			return (1-this.probability)/this.cost;
		}

	}

	public void setProbability(double p){
		this.probability=p;
	}
	public void setCost(double c){
		this.cost=c;
	}
	public void setParent(Node parent){
		this.parent=parent;
	}

	public String getNames(){
		return names.remove(0);
	}

	public Double mul(List<Double> a){
		double product=1.0;
		for(int i=0; i<a.size(); i++){
			product*=a.get(i);
		}
		return product;
	}



	public void fixTree(Node a){
		for(int i=0; i<a.getChildren().size(); i++){
			a.getChildren().get(i).setParent(a);
			fixTree(a.getChildren().get(i));
		}
		for(int i=0; i<a.getLeafs().size(); i++){
			a.getLeafs().get(i).setParent(a);
		}
	}

	public void simplifyTree(Node a){
		List<Node> remove= new ArrayList<Node>();
		for(int i=0; i<a.getChildren().size(); i++){
			simplifyTree(a.getChildren().get(i));

			if(a.getChildren().get(i).getFunction()==a.getFunction()){
				for(int j=0; j<a.getChildren().size(); j++){
					a.addChildNode(a.getChildren().get(j));
				}
				for(int k=0; k<a.getChildren().get(i).getLeafs().size(); k++){
					a.addLeafNode(a.getChildren().get(i).getLeafs().get(k));
					remove.add(a.getChildren().get(i));
				}
			}
		}
		for(int l=0; l<remove.size(); l++){
			a.removeChild(remove.get(l));
		}
	}

//Confuse about Vals...
	public void setLeaf(Node a, List<Leaf> b){
		int where=0;
		if(b.size()==0){
			for(int i=0; i<a.getLeafs().size(); i++){
				for(int j=0; j<b.size(); j++){
					if(b.get(j).getName().equals(a.getLeafs().get(i).getName())){
						where=j;
					}
				}
				
				a.getLeafs().get(i).setProbability(b.get(where).getProbability());
				a.getLeafs().get(i).setCost(b.get(where).getCost());
			}
			
			for(int i=0; i<a.getChildren().size(); i++){
				setLeaf(a.getChildren().get(i), b);
			}
		}
		/*
		else{
			for(int i=0; i<a.getLeafs().size(); i++){
			System.out.print("Leaf{}".);
		}
	*/
		//I'm confuse about the else statement here. What is the format method, I know it has something to do with strings
	
	   
	
	}
	/*
	 * Missing printTree and createTree method. I am confuse about those
	 */
	
	
	
	
	
	


}










