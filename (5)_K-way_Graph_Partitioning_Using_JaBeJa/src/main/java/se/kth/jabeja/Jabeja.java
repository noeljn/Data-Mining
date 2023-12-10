package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class Jabeja {
  final static Logger logger = Logger.getLogger(Jabeja.class);
  private final Config config;
  private final HashMap<Integer/*id*/, Node/*neighbors*/> entireGraph;
  private final List<Integer> nodeIds;
  private int numberOfSwaps;
  private int round;
  private float T;
  private boolean resultFileCreated = false;
  private int rounds = 0;
  private final float min_T = (float) 0.00001;
  // ___Settings___
  // Enable (true) or disable (false) the following settings to test different set-ups. 
  private boolean newAnnealing = true;  // Use new annealing function
  private boolean task2_2 = true;       // Reset temperature to 1 every 400 rounds
  private boolean bonusTaskVer1 = true; // Decrease temperature 
  private boolean bonusTaskVer2 = true; // Gaussian distribution

  //-------------------------------------------------------------------
  public Jabeja(HashMap<Integer, Node> graph, Config config) {
    this.entireGraph = graph;
    this.nodeIds = new ArrayList(entireGraph.keySet());
    this.round = 0;
    this.numberOfSwaps = 0;
    this.config = config;
    if (newAnnealing) {
      config.setDelta((float) 0.9); // test1=0.9; test2=0.8
      config.setTemperature((float) 1);
    } else {
      config.setDelta((float) 0.003);
    }
    this.T = config.getTemperature();
  }


  //-------------------------------------------------------------------
  public void startJabeja() throws IOException {
    for (round = 0; round < config.getRounds(); round++) {
      for (int id : entireGraph.keySet()) {
        sampleAndSwap(id);
      }

      //one cycle for all nodes have completed.
      //reduce the temperature
      saCoolDown();
      report();
    }
  }

  /**
   * Simulated analealing cooling function
   */
  private void saCoolDown() {
    // TODO for second task
    if (newAnnealing) {
      rounds++;
      if (T > min_T) {
        T = customTemperatureReduction(rounds);
      } 
      else { // When T is smaller than the minimum temperature, 
        T = min_T;
      }
      
      if (rounds % 400 == 0  && task2_2) {
        T = 1;
        //rounds = 0;
        
      }
    } 
    else {
      if (T > 1)
        T -= config.getDelta();
      if (T < 1)
        T = 1;
    }

  }

  private float customTemperatureReduction(int round) {
    // For bonus task
    if (bonusTaskVer1) {
      return T *= 1000 / (1000 + round/3); 
    }
    else {
      return T *= config.getDelta();}
  }

  private double getAcceptanceProbability(double oldDegree, double newDegree) {
    // The acceptance probability function receives the previous cost, the new cost,
    // and the present temperature, then outputs a value ranging from 0 to 1.
    // This value serves as an advisory on the advisability of transitioning to the new solution.

    if (bonusTaskVer2) {
      return Math.exp((1 / oldDegree - 1 / newDegree) / T);
    }
    else {
      return Math.exp((newDegree - oldDegree) / T); 
    }
    
  }

  /**
   * Sample and swap algorith at node p
   * @param nodeId
   */ 
  private void sampleAndSwap(int nodeId) {
    Node partner = null;
    Node nodep = entireGraph.get(nodeId);

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL) {
      // swap with random neighbors
      // TODO
      partner = findPartner(nodeId, getNeighbors(nodep));
    }

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM) {
      // if local policy fails then randomly sample the entire graph
      // TODO
      if (partner == null)
        partner = findPartner(nodeId, getSample(nodeId));
    }

    // swap the colors
    // TODO
    if (partner != null) {
      int tmpColor = nodep.getColor();
      nodep.setColor(partner.getColor());
      partner.setColor(tmpColor);
      numberOfSwaps++;
    }
  }

  public Node findPartner(int nodeId, Integer[] nodes){

    Node nodep = entireGraph.get(nodeId);
    float alpha = config.getAlpha();

    Node bestPartner = null;
    double highestBenefit = 0;

    // TODO
    for (int node : nodes) {
      Node nodeq = entireGraph.get(node);
      int nodeppDegree = getDegree(nodep, nodep.getColor());
      int nodeqqDegree = getDegree(nodeq, nodeq.getColor());

      double oldDegree = Math.pow(nodeppDegree, alpha) + Math.pow(nodeqqDegree, alpha);

      int nodepqDegree = getDegree(nodep, nodeq.getColor());
      int nodeqpDegree = getDegree(nodeq, nodep.getColor());

      double newDegree = Math.pow(nodepqDegree, alpha) + Math.pow(nodeqpDegree, alpha);

      if (newAnnealing) {
        Random random = new Random();
        double acceptanceProbability = getAcceptanceProbability(oldDegree, newDegree);
        if (acceptanceProbability > random.nextDouble() 
            && newDegree != oldDegree 
            && acceptanceProbability > highestBenefit) {
          bestPartner = nodeq;
          highestBenefit = acceptanceProbability;
        }
      } 
      else {
        if ((newDegree * T > oldDegree) && (newDegree > highestBenefit)) {
          bestPartner = nodeq;
          highestBenefit = newDegree;
        }
      }
    }

    return bestPartner;
  }

  /**
   * The the degreee on the node based on color
   * @param node
   * @param colorId
   * @return how many neighbors of the node have color == colorId
   */
  private int getDegree(Node node, int colorId){
    int degree = 0;
    for(int neighborId : node.getNeighbours()){
      Node neighbor = entireGraph.get(neighborId);
      if(neighbor.getColor() == colorId){
        degree++;
      }
    }
    return degree;
  }

  /**
   * Returns a uniformly random sample of the graph
   * @param currentNodeId
   * @return Returns a uniformly random sample of the graph
   */
  private Integer[] getSample(int currentNodeId) {
    int count = config.getUniformRandomSampleSize();
    int rndId;
    int size = entireGraph.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    while (true) {
      rndId = nodeIds.get(RandNoGenerator.nextInt(size));
      if (rndId != currentNodeId && !rndIds.contains(rndId)) {
        rndIds.add(rndId);
        count--;
      }

      if (count == 0)
        break;
    }

    Integer[] ids = new Integer[rndIds.size()];
    return rndIds.toArray(ids);
  }

  /**
   * Get random neighbors. The number of random neighbors is controlled using
   * -closeByNeighbors command line argument which can be obtained from the config
   * using {@link Config#getRandomNeighborSampleSize()}
   * @param node
   * @return
   */
  private Integer[] getNeighbors(Node node) {
    ArrayList<Integer> list = node.getNeighbours();
    int count = config.getRandomNeighborSampleSize();
    int rndId;
    int index;
    int size = list.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    if (size <= count)
      rndIds.addAll(list);
    else {
      while (true) {
        index = RandNoGenerator.nextInt(size);
        rndId = list.get(index);
        if (!rndIds.contains(rndId)) {
          rndIds.add(rndId);
          count--;
        }

        if (count == 0)
          break;
      }
    }

    Integer[] arr = new Integer[rndIds.size()];
    return rndIds.toArray(arr);
  }


  /**
   * Generate a report which is stored in a file in the output dir.
   *
   * @throws IOException
   */
  private void report() throws IOException {
    int grayLinks = 0;
    int migrations = 0; // number of nodes that have changed the initial color
    int size = entireGraph.size();

    for (int i : entireGraph.keySet()) {
      Node node = entireGraph.get(i);
      int nodeColor = node.getColor();
      ArrayList<Integer> nodeNeighbours = node.getNeighbours();

      if (nodeColor != node.getInitColor()) {
        migrations++;
      }

      if (nodeNeighbours != null) {
        for (int n : nodeNeighbours) {
          Node p = entireGraph.get(n);
          int pColor = p.getColor();

          if (nodeColor != pColor)
            grayLinks++;
        }
      }
    }

    int edgeCut = grayLinks / 2;

    logger.info("round: " + round +
            ", edge cut:" + edgeCut +
            ", swaps: " + numberOfSwaps +
            ", migrations: " + migrations);

    saveToFile(edgeCut, migrations);
  }

  private void saveToFile(int edgeCuts, int migrations) throws IOException {
    String delimiter = "\t\t";
    String outputFilePath;

    //output file name
    File inputFile = new File(config.getGraphFilePath());
    outputFilePath = config.getOutputDir() +
            File.separator +
            inputFile.getName() + "_" +
            "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
            "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
            "T" + "_" + config.getTemperature() + "_" +
            "D" + "_" + config.getDelta() + "_" +
            "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
            "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
            "A" + "_" + config.getAlpha() + "_" +
            "R" + "_" + config.getRounds() + ".txt";

    if (!resultFileCreated) {
      File outputDir = new File(config.getOutputDir());
      if (!outputDir.exists()) {
        if (!outputDir.mkdir()) {
          throw new IOException("Unable to create the output directory");
        }
      }
      // create folder and result file with header
      String header = "# Migration is number of nodes that have changed color.";
      header += "\n\nRound" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations" + delimiter + "Skipped" + "\n";
      FileIO.write(header, outputFilePath);
      resultFileCreated = true;
    }

    FileIO.append(round + delimiter + (edgeCuts) + delimiter + numberOfSwaps + delimiter + migrations + "\n", outputFilePath);
  }
}

