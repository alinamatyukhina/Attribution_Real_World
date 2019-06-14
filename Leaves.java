package leaves;


import com.github.javaparser.*;
import com.github.javaparser.ast.body.*; 
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.ArrayCreationLevel;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.AnnotationDeclaration;
import com.github.javaparser.ast.body.AnnotationMemberDeclaration;
import com.github.javaparser.ast.body.BodyDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.JavadocComment;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.stmt.AssertStmt;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.BreakStmt;
import com.github.javaparser.ast.stmt.CatchClause;
import com.github.javaparser.ast.stmt.ContinueStmt;
import com.github.javaparser.ast.stmt.DoStmt;
import com.github.javaparser.ast.stmt.EmptyStmt;
import com.github.javaparser.ast.stmt.ExplicitConstructorInvocationStmt;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.ForeachStmt;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.stmt.LabeledStmt;
import com.github.javaparser.ast.stmt.LocalClassDeclarationStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.stmt.SwitchEntryStmt;
import com.github.javaparser.ast.stmt.SwitchStmt;
import com.github.javaparser.ast.stmt.SynchronizedStmt;
import com.github.javaparser.ast.stmt.ThrowStmt;
import com.github.javaparser.ast.stmt.TryStmt;
import com.github.javaparser.ast.stmt.WhileStmt;
import com.github.javaparser.ast.type.ArrayType;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.type.IntersectionType;
import com.github.javaparser.ast.type.PrimitiveType;
import com.github.javaparser.ast.type.Type;
import com.github.javaparser.ast.type.TypeParameter;
import com.github.javaparser.ast.type.UnionType;
import com.github.javaparser.ast.type.UnknownType;
import com.github.javaparser.ast.type.VoidType;
import com.github.javaparser.ast.type.WildcardType;
import com.github.javaparser.ast.visitor.ModifierVisitor;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.Visitable;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.printer.ConcreteSyntaxModel;
import com.github.javaparser.printer.concretesyntaxmodel.CsmElement;
import com.github.javaparser.printer.lexicalpreservation.LexicalPreservingPrinter;
import com.github.javaparser.utils.Pair;
import java.util.Optional;
import java.util.Random;
import java.util.StringTokenizer;
import com.vacowin.author.util.*;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Pattern;  

import com.github.javaparser.*;
import com.github.javaparser.ast.Node;

import javax.annotation.*;
import java.util.HashMap;
import java.util.function.Consumer;

import static com.github.javaparser.JavaToken.Category.*;
import javax.*;

import com.github.javaparser.symbolsolver.javaparsermodel.JavaParserFacade;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;



/* program to parse a java source code file, collect all the different AST node types and print count for each node type
 *  authored by Celine Perley
 *  
 *  08/09/2017--update
 *  
 *  ------implemented only in integer literals and simple name classes for now----
 *  
 *  -- uses getParentNode 
 *  -- uses map to keep track of count each particular type of node
 *  -- determines leaf node frequency by dividing leaf node count by total amount of leaf nodes
 *  -- prints out leaf information into separate file (leaf.txt) (need to update manually)
 *  
 *  
 */


/**
 * 	@author Omar Hussein
 * 	Modified on: 01/08/2018 -- Added functionality
 * 	FS2WS: Iterates through the file and convert every ForStmt into a WhileStmt - uses other mini-helper functions
 * 	WS2FS: Iterates through the file and convert every WhileStmt into a Forstmt - uses other mini-helper functions
 * 	switchOBFS: Iterates through the file and convert every WhileStmt into ForStmt; Then transforms every ForStmt in
 * 				SwitchStmt. - uses other mini-helper functions
 * 	used com.vacowin.author.util
 * 		-Used source code from TokenUtil.java
 * 		-Used ideas from TransformVarUtil
 * 		The library was really helpful in gaining ideas and understanding how to manipulate code
 *
 */


public class Leaves {

	

	private static  Map<String, Integer> leafMap = new HashMap<String, Integer>(); 
	
	 
	
	
	//inner classes for each AST node type. Each class overrides the visit method and collects the nodes
	//LeafNodes are collected in a separate arraylist
		
	private static class AnnotationCollector extends VoidVisitorAdapter <List<String>> {
		
		
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(AnnotationDeclaration ad, List<String> collector) {
		 super.visit(ad, collector);
		 collector.add(ad.getNameAsString());
		 
		 if(ad.getChildNodes().isEmpty()) {
					leafNodes.add(ad.toString());
		 }
		 }
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
			 
		 }
		 
		 }
	
	
	private static class AnnotationMemberCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		
		 @Override
		 public void visit(AnnotationMemberDeclaration amd, List<String> collector) {
			 super.visit(amd, collector);
			 collector.add(amd.getNameAsString());
			
			 if(amd.getChildNodes().isEmpty()) {
				leafNodes.add(amd.toString()); 
			 }
			 
		 }
		 
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
			 
		 }
		 }
	
	
	private static class ArrayAccessExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		
		 @Override
		 public void visit(ArrayAccessExpr aae, List<String> collector) {
		 super.visit(aae, collector);
		 collector.add(aae.toString());
		
		 if(aae.getChildNodes().isEmpty()) {
						
			 leafNodes.add(aae.toString());
			 
		 }
		 
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
			 
		 }
		 }
	
	//could also use getNodesLists() and getMetaModel(), getRange()
	private static class ArrayCreationExprCollector extends VoidVisitorAdapter <List<String>> {
		
		
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ArrayCreationExpr ace, List<String> collector) {
		 super.visit(ace, collector);
		 collector.add(ace.toString()); 
		 
		 if(ace.getChildNodes().isEmpty()) {
				leafNodes.add(ace.toString()); 
		 }
		 }
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
		 }
		 
	} 
	
	private static class ArrayCreationLevelCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ArrayCreationLevel acl, List<String> collector) {
		 super.visit(acl, collector);
		 collector.add(acl.toString()); 
		 
		 if(acl.getChildNodes().isEmpty()) {
				leafNodes.add(acl.toString()); 
		 }
		 
		 }
		 
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
		 }
		 }
	

	private static class ArrayInitializerExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ArrayInitializerExpr aie, List<String> collector) {
		 super.visit(aie, collector);
		 collector.add(aie.toString());
		 
		 if(aie.getChildNodes().isEmpty()) {
				leafNodes.add(aie.toString()); 
		 }
		 }
		 
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	
	private static class ArrayTypeCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ArrayType at, List<String> collector) {
		 super.visit(at, collector);
		 collector.add(at.asString()); 
		 
		 if(at.getChildNodes().isEmpty()) {
				leafNodes.add(at.toString());
		 }
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
		 
	
	

	private static class AssertStmtCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(AssertStmt astmt, List<String> collector) {
		 super.visit(astmt, collector);
		 collector.add(astmt.toString()); 
		 
		 if(astmt.getChildNodes().isEmpty()) {
				leafNodes.add(astmt.toString());
		 }
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	
	private static class AssignExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(AssignExpr aexpr, List<String> collector) {
		 super.visit(aexpr, collector);
		 collector.add(aexpr.toString());
		
		 if(aexpr.getChildNodes().isEmpty()) {
				leafNodes.add(aexpr.toString());
		 }
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 
		 }
	
	
	private static class BinaryExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(BinaryExpr bexpr, List<String> collector) {
		 super.visit(bexpr, collector);
		 collector.add(bexpr.toString()); 
		 
		 if(bexpr.getChildNodes().isEmpty()) {
				leafNodes.add(bexpr.toString());
		 }
		 
		 }	
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	//not sure if this needs leafNode check
	private static class BlockCommentCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(BlockComment blkcom, List<String> collector) {
		 super.visit(blkcom, collector);
		 collector.add(blkcom.toString());
		 
		 if(blkcom.getChildNodes().isEmpty()) {
				leafNodes.add(blkcom.toString()); 	
		 }
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class BlockStmtCollector extends VoidVisitorAdapter <List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(BlockStmt blkstmt, List<String> collector) {
	     super.visit(blkstmt, collector);
	     collector.add(blkstmt.toString());
	    
		 if(blkstmt.getChildNodes().isEmpty()) {
				leafNodes.add(blkstmt.toString());
		 }
		 
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class BooleanLiteralExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(BooleanLiteralExpr booleanLitExpr, List<String> collector) {
	     super.visit(booleanLitExpr, collector);
	     collector.add(booleanLitExpr.toString());
	     
		 if(booleanLitExpr.getChildNodes().isEmpty()) {
				leafNodes.add(booleanLitExpr.toString());
		 }
		 
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	
	private static class BreakStmtCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(BreakStmt brkStmt, List<String> collector) {
	     super.visit(brkStmt, collector);
	     collector.add(brkStmt.toString());
	     
		 if(brkStmt.getChildNodes().isEmpty()) {
				leafNodes.add(brkStmt.toString());
		 }
		 
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class CastExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(CastExpr cexpr, List<String> collector) {
	     super.visit(cexpr, collector);
	     collector.add(cexpr.toString());
	     
		 if(cexpr.getChildNodes().isEmpty()) {
				leafNodes.add(cexpr.toString());	
		 }
		 
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class CatchClauseCollector extends VoidVisitorAdapter <List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(CatchClause cc, List<String> collector) {
	     super.visit(cc, collector);
	     collector.add(cc.toString());
	    
		 if(cc.getChildNodes().isEmpty()) {
				leafNodes.add(cc.toString());
		 }
		 
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class CharLiteralExprCollector extends VoidVisitorAdapter <List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(CharLiteralExpr charLitExpr, List<String> collector) {
	     super.visit(charLitExpr, collector);
	     collector.add(charLitExpr.toString());
	 
		 if(charLitExpr.getChildNodes().isEmpty()) {
				leafNodes.add(charLitExpr.toString());
		 }
		 
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	
	private static class ClassExprCollector extends VoidVisitorAdapter <List<String>> {
		
		 public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ClassExpr classExpr, List<String> collector) {
	     super.visit(classExpr, collector);
	     collector.add(classExpr.toString());
	     
		 if(classExpr.getChildNodes().isEmpty()) {
				leafNodes.add(classExpr.toString());	
		 }
		 
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ClassOrInterfaceDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ClassOrInterfaceDeclaration coid, List<String> collector) {
		 super.visit(coid, collector);
		 collector.add(coid.getNameAsString());
		
		 if(coid.getChildNodes().isEmpty()) {
				leafNodes.add(coid.toString());	
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class ClassOrInterfaceTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ClassOrInterfaceType coit, List<String> collector) {
		 super.visit(coit, collector);
		 collector.add(coit.toString());
		
		 if(coit.getChildNodes().isEmpty()) {
				leafNodes.add(coit.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class CompilationUnitCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		
		 @Override
		 public void visit(CompilationUnit cu, List<String> collector) {
		 super.visit(cu, collector);
		 collector.add(cu.toString());
		
		 if(cu.getChildNodes().isEmpty()) {
				leafNodes.add(cu.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ConditionalExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ConditionalExpr condExpr, List<String> collector) {
		 super.visit(condExpr, collector);
		 collector.add(condExpr.toString());
		
		 if(condExpr.getChildNodes().isEmpty()) {
				leafNodes.add(condExpr.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ConstructorDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ConstructorDeclaration conDec, List<String> collector) {
		 super.visit(conDec, collector);
		 collector.add(conDec.toString());
		 
		 if(conDec.getChildNodes().isEmpty()) {
				leafNodes.add(conDec.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class ContinueStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ContinueStmt conStmt, List<String> collector) {
		 super.visit(conStmt, collector);
		 collector.add(conStmt.toString());
		
		 if(conStmt.getChildNodes().isEmpty()) {
				leafNodes.add(conStmt.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class DoStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(DoStmt dStmt, List<String> collector) {
		 super.visit(dStmt, collector);
		 collector.add(dStmt.toString());
		 
		 if(dStmt.getChildNodes().isEmpty()) {
				leafNodes.add(dStmt.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class DoubleLiteralExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(DoubleLiteralExpr dLitExpr, List<String> collector) {
		 super.visit(dLitExpr, collector);
		 collector.add(dLitExpr.toString());
		 
		 if(dLitExpr.getChildNodes().isEmpty()) {
				leafNodes.add(dLitExpr.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class EmptyStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(EmptyStmt empStmt, List<String> collector) {
		 super.visit(empStmt, collector);
		 collector.add(empStmt.toString());
		
		 if(empStmt.getChildNodes().isEmpty()) {
				leafNodes.add(empStmt.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class EnclosedExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		
		 @Override
		 public void visit(EnclosedExpr enclExpr, List<String> collector) {
		 super.visit(enclExpr, collector);
		 collector.add(enclExpr.toString());
		 
		 if(enclExpr.getChildNodes().isEmpty()) {
				leafNodes.add(enclExpr.toString());	
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class EnumConstantDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(EnumConstantDeclaration ecd, List<String> collector) {
		 super.visit(ecd, collector);
		 collector.add(ecd.toString());
		 
		 if(ecd.getChildNodes().isEmpty()) {
				leafNodes.add(ecd.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class EnumDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(EnumDeclaration ed, List<String> collector) {
		 super.visit(ed, collector);
		 collector.add(ed.toString());
		
		 if(ed.getChildNodes().isEmpty()) {
				leafNodes.add(ed.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ExplicitConstructorInvocationStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ExplicitConstructorInvocationStmt ecis, List<String> collector) {
		 super.visit(ecis, collector);
		 collector.add(ecis.toString());
		 
		 if(ecis.getChildNodes().isEmpty()) {
				leafNodes.add(ecis.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ExpressionStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ExpressionStmt exStmt, List<String> collector) {
		 super.visit(exStmt, collector);
		 collector.add(exStmt.toString());
		 
		 if(exStmt.getChildNodes().isEmpty()) {
				leafNodes.add(exStmt.toString());	
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class FieldDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(FieldDeclaration fd, List<String> collector) {
		 super.visit(fd, collector);
		 collector.add(fd.toString());
		 
		 if(fd.getChildNodes().isEmpty()) {
				leafNodes.add(fd.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class FieldAccessExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(FieldAccessExpr fae, List<String> collector) {
		 super.visit(fae, collector);
		 collector.add(fae.toString());
		 
		 if(fae.getChildNodes().isEmpty()) {
				leafNodes.add(fae.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ForStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
	//	public List<Expression> test = new ArrayList<>();
		
		
		
		 @Override
		 public void visit(ForStmt fStmt, List<String> collector) {
		 super.visit(fStmt, collector);
		
	//	test = fStmt.getInitialization();
		
		//Prints out the for statement with its body
		 collector.add(fStmt.toString());
		 
		//prints out the init: int i = 2
	//	collector.add(test.get(0).toString());
		
		 //prints out the comparing i < 100
	//	 collector.add(fStmt.getCompare().toString());
		
		  //prints out the update factor: i++
	//	  collector.add(fStmt.getUpdate().get(0).toString());
		
		
		
		 		 
		 
		 
		 if(fStmt.getChildNodes().isEmpty()) {
				leafNodes.add(fStmt.toString());
		 }
		 
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ForeachStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ForeachStmt feStmt, List<String> collector) {
		 super.visit(feStmt, collector);
		 collector.add(feStmt.toString());
		 
		 if(feStmt.getChildNodes().isEmpty()) {
				leafNodes.add(feStmt.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class IfStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(IfStmt ifStmt, List<String> collector) {
		 super.visit(ifStmt, collector);
		 collector.add(ifStmt.toString());
		 
		 if(ifStmt.getChildNodes().isEmpty()) {
				leafNodes.add(ifStmt.toString());	
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ImportDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ImportDeclaration id, List<String> collector) {
		 super.visit(id, collector);
		 collector.add(id.toString());
		 
		 if(id.getChildNodes().isEmpty()) {
				leafNodes.add(id.toString());	
		 }
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class InitializerDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(InitializerDeclaration ind, List<String> collector) {
		 super.visit(ind, collector);
		 collector.add(ind.toString());
		 
		 if(ind.getChildNodes().isEmpty()) {
				leafNodes.add(ind.toString());
		 }
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	
	private static class InstanceOfExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(InstanceOfExpr ie, List<String> collector) {
		 super.visit(ie, collector);
		 collector.add(ie.toString());
		 
		 if(ie.getChildNodes().isEmpty()) {
				leafNodes.add(ie.toString());
		 }
		 
		 
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 
	}
	
	private static class IntegerLiteralExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>(); 
		public List<String> parentNodes = new ArrayList<>();
		 @Override
		 public void visit(IntegerLiteralExpr ile, List<String> collector) {
		 super.visit(ile, collector);
		 
		 collector.add(ile.toString());
		 
		 if(ile.getChildNodes().isEmpty()) {
			leafNodes.add(ile.toString() +"\n");
			parentNodes.add(" Parent Node of " + ile.toString() + " : " + ile.getParentNode().get().toString() + "\n"); 
					
		 }
		
	}
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }	 
		 
		 
		 public List<String> getParentNodes(){
			 
			 return parentNodes; 
			 
		 }
		 
		 
		 
		 
		 
		 
		 
	}
		 
		 
		 
		 
	
	private static class IntersectionTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>(); 
		
		 @Override
		 public void visit(IntersectionType it, List<String> collector) {
		 super.visit(it, collector);
		 collector.add(it.toString());
		 
		 if(it.getChildNodes().isEmpty()) {
				leafNodes.add(it.toString());
			}
		 }
		 
		
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }	
		 
		 
		 
		 }
	
	private static class JavadocCommentCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>(); 
		 @Override
		 public void visit(JavadocComment javadoc, List<String> collector) {
		 super.visit(javadoc, collector);
		 collector.add(javadoc.toString());
		 
		 if(javadoc.getChildNodes().isEmpty()) {
				leafNodes.add(javadoc.toString());	
				
			}
		
		 }
		 

		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class LambdaExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(LambdaExpr lambaExpr, List<String> collector) {
		 super.visit(lambaExpr, collector);
		 collector.add(lambaExpr.toString());
		 
		 if(lambaExpr.getChildNodes().isEmpty()) {
				leafNodes.add(lambaExpr.toString());
			
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class LabeledStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(LabeledStmt lStmt, List<String> collector) {
		 super.visit(lStmt, collector);
		 collector.add(lStmt.toString());
		 
		 if(lStmt.getChildNodes().isEmpty()) {
				leafNodes.add(lStmt.toString());	
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class LineCommentCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(LineComment lineCom, List<String> collector) {
		 super.visit(lineCom, collector);
		 collector.add(lineCom.toString());
		 
		 if(lineCom.getChildNodes().isEmpty()) {
				leafNodes.add(lineCom.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class LocalClassDeclarationStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(LocalClassDeclarationStmt lcdStmt, List<String> collector) {
		 super.visit(lcdStmt, collector);
		 collector.add(lcdStmt.toString());
		 
		 if(lcdStmt.getChildNodes().isEmpty()) {
				leafNodes.add(lcdStmt.toString());	
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class LongLiteralExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(LongLiteralExpr lle, List<String> collector) {
		 super.visit(lle, collector);
		 collector.add(lle.toString());
		 
		 if(lle.getChildNodes().isEmpty()) {
				leafNodes.add(lle.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	
	
	private static class MarkerAnnotationExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(MarkerAnnotationExpr mae, List<String> collector) {
		 super.visit(mae, collector);
		 collector.add(mae.toString());
		 
		 if(mae.getChildNodes().isEmpty()) {
				leafNodes.add(mae.toString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class MemberValuePairCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(MemberValuePair mvp, List<String> collector) {
		 super.visit(mvp, collector);
		 collector.add(mvp.toString());
		 
		 if(mvp.getChildNodes().isEmpty()) {
				leafNodes.add(mvp.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class MethodCallExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(MethodCallExpr mcexpr, List<String> collector) {
		 super.visit(mcexpr, collector);
		 collector.add(mcexpr.toString());
		 
		 if(mcexpr.getChildNodes().isEmpty()) {
				leafNodes.add(mcexpr.toString());	
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class MethodNameCollector extends VoidVisitorAdapter <List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(MethodDeclaration md, List<String> collector) {
		 super.visit(md, collector);
		 collector.add(md.getNameAsString());
		 
		 if(md.getChildNodes().isEmpty()) {
				leafNodes.add(md.getNameAsString()); 
		 }
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class MethodReferenceExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(MethodReferenceExpr mrexpr, List<String> collector) {
		 super.visit(mrexpr, collector);
		 collector.add(mrexpr.toString());
		 
		 if(mrexpr.getChildNodes().isEmpty()) {
				leafNodes.add(mrexpr.toString());	
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	private static class NameCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(Name n, List<String> collector) {
		 super.visit(n, collector);
		 collector.add(n.toString());
		 
		 if(n.getChildNodes().isEmpty()) {
				leafNodes.add(n.toString());	
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class NameExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(NameExpr nexpr, List<String> collector) {
		 super.visit(nexpr, collector);
		 collector.add(nexpr.toString());
		 
		 if(nexpr.getChildNodes().isEmpty()) {
				leafNodes.add(nexpr.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	

	//nodelist does not have getChildrenNodes --> always has children? 
	private static class NodeListCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(NodeList nl, List<String> collector) {
		 super.visit(nl, collector);
		 collector.add(nl.toString());
		 List<String> leafNodes = new ArrayList<>();
	/*	 if(nl.getChildNodes().isEmpty()) {
				
		 }
		*/ 
		 }
		 }
	
	private static class NormalAnnotationExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(NormalAnnotationExpr naexpr, List<String> collector) {
		 super.visit(naexpr, collector);
		 collector.add(naexpr.toString());
		 
		 if(naexpr.getChildNodes().isEmpty()) {
			leafNodes.add(naexpr.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class NullLiteralExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(NullLiteralExpr nuexpr, List<String> collector) {
		 super.visit(nuexpr, collector);
		 collector.add(nuexpr.toString());
		 
		 if(nuexpr.getChildNodes().isEmpty()) {
				leafNodes.add(nuexpr.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 
		 }
	
	private static class ObjectCreationExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(ObjectCreationExpr ocexpr, List<String> collector) {
		 super.visit(ocexpr, collector);
		 collector.add(ocexpr.toString());
		 
		 if(ocexpr.getChildNodes().isEmpty()) {
				leafNodes.add(ocexpr.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class PackageDeclarationCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(PackageDeclaration pd, List<String> collector) {
		 super.visit(pd, collector);
		 collector.add(pd.toString());
		 
		 if(pd.getChildNodes().isEmpty()) {
				leafNodes.add(pd.toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	private static class ParameterCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(Parameter p, List<String> collector) {
		 super.visit(p, collector);
		 collector.add(p.toString());
		
		 if(p.getChildNodes().isEmpty()) {
				leafNodes.add(p.getNameAsString());
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 }
	
	

	
	private static class PrimitiveTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(PrimitiveType pt, List<String> collector) {
		 super.visit(pt, collector);
		 collector.add(pt.toString());
		 
		 if(pt.getChildNodes().isEmpty()) {
				leafNodes.add(pt.toString());	
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 return leafNodes; 
		 }
		 
		 }
	
	
	private static class SimpleNameCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> parentNodes = new ArrayList<>();
		public List<String> leafNodes = new ArrayList<>();
		 @Override
		 public void visit(SimpleName sn, List<String> collector) {
		 super.visit(sn, collector);
		 collector.add(sn.toString());
		 
		 if(sn.getChildNodes().isEmpty()) {
			 leafNodes.add(sn.toString());
			 parentNodes.add(" Parent Node of " + sn.toString() + " : " + sn.getParentNode().get().toString()+ "\n");
		 }
		
		 }
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
			 
		 }
		 
		 public List<String> getParentNodes(){
			 
			 return parentNodes; 
			 
		 }
		 
		 
		 }
	
	private static class SingleMemberAnnotationExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public  List<String> leafNodes = new ArrayList<>();
		public  List<String> parentNodes = new ArrayList<>();
		 @Override
		 public void visit(SingleMemberAnnotationExpr smaexpr, List<String> collector) {
		 super.visit(smaexpr, collector);
		 collector.add(smaexpr.toString());
		
		 if(smaexpr.getChildNodes().isEmpty()) {
				leafNodes.add(smaexpr.getNameAsString());	
				parentNodes.add(" Parent Node of " + smaexpr.toString() + " : " + smaexpr.getParentNode().get().toString());
		 }
		
		 }
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
			 
		 }
		 
		 public List<String> getParentNodes(){
			 
			 return parentNodes; 
			 
		 }
		 }
	
	private static class StringLiteralExprCollector extends VoidVisitorAdapter<List<String>> {
		
		
		public List<String> leafNodes = new ArrayList<>();
		
		 @Override
		 public void visit(StringLiteralExpr stexpr, List<String> collector) {
		 super.visit(stexpr, collector);
		 collector.add(stexpr.toString());
		 
		 if(stexpr.getChildNodes().isEmpty()) {
			 leafNodes.add(stexpr.toString()); 
			 
			 
		 }
		 }
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
			 
		 }
		 
		 
		 }
	
	private static class SuperExprCollector extends VoidVisitorAdapter<List<String>> {
		
		public List<String> leafNodes = new ArrayList<>(); 
		 @Override
		 public void visit(SuperExpr suexpr, List<String> collector) {
		 super.visit(suexpr, collector);
		 collector.add(suexpr.toString());
		
		 }
		 
		 public List<String> getLeafNodes(){
			 
			 return leafNodes; 
			 
		 }
		 
		
		 }
		 
	
	private static class SynchronizedStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(SynchronizedStmt synchStmt, List<String> collector) {
		 super.visit(synchStmt, collector);
		 collector.add(synchStmt.toString());
		
		 }
		 }
	
	private static class SwitchEntryStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(SwitchEntryStmt sweStmt, List<String> collector) {
		 super.visit(sweStmt, collector);
		 collector.add(sweStmt.toString());
		
		 }
		 }
	
	private static class SwitchStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(SwitchStmt swStmt, List<String> collector) {
		 super.visit(swStmt, collector);
		 collector.add(swStmt.toString());
		
		 }
		 }
	
	private static class ThisExprCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(ThisExpr thisexpr, List<String> collector) {
		 super.visit(thisexpr, collector);
		 collector.add(thisexpr.toString());
		
		 }
		 }
	
	private static class ThrowStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(ThrowStmt thrwStmt, List<String> collector) {
		 super.visit(thrwStmt, collector);
		 collector.add(thrwStmt.toString());
		
		 }
		 }
	
	private static class TryStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(TryStmt tryStmt, List<String> collector) {
		 super.visit(tryStmt, collector);
		 collector.add(tryStmt.toString());
		
		 }
		 }
	
	private static class TypeExprCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(TypeExpr typexpr, List<String> collector) {
		 super.visit(typexpr, collector);
		 collector.add(typexpr.toString());
		
		 }
		 }
	
	private static class TypeParameterCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(TypeParameter typParam, List<String> collector) {
		 super.visit(typParam, collector);
		 collector.add(typParam.toString());
		
		 }
		 }
	
	private static class UnaryExprCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(UnaryExpr uexpr, List<String> collector) {
		 super.visit(uexpr, collector);
		 collector.add(uexpr.toString());
		
		 }
		 }
	
	private static class UnionTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(UnionType uType, List<String> collector) {
		 super.visit(uType, collector);
		 collector.add(uType.toString());
		
		 }
		 }
	
	private static class UnknownTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(UnknownType unkwnType, List<String> collector) {
		 super.visit(unkwnType, collector);
		 collector.add(unkwnType.toString());
		
		 }
		 }
	
	
	
	private static class VariableDeclarationExprCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(VariableDeclarationExpr vdexpr, List<String> collector) {
		 super.visit(vdexpr, collector);
		 collector.add(vdexpr.toString());
		 List<String> leafNodes = new ArrayList<>(); 
		 
		
		 }
		 }
	
	private static class VariableDeclaratorCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(VariableDeclarator vd, List<String> collector) {
		 super.visit(vd, collector);
		 collector.add(vd.toString());
		 List<String> leafNodes = new ArrayList<>(); 
		
		 
		 
		 
		
		 }
		 }
	
	private static class VoidTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(VoidType vt, List<String> collector) {
		 super.visit(vt, collector);
		 collector.add(vt.toString());
		
		 }
		 }
	
	private static class WhileStmtCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(WhileStmt wStmt, List<String> collector) {
		 super.visit(wStmt, collector);
		 
	
		 
		 
		 collector.add(wStmt.toString());
		 collector.add(wStmt.getBody().toString());
		 collector.add(wStmt.getCondition().toString());
		 
		 
		 
		 }
		 }
	
	private static class WildcardTypeCollector extends VoidVisitorAdapter<List<String>> {
		
		 @Override
		 public void visit(WildcardType wldType, List<String> collector) {
		 super.visit(wldType, collector);
		 collector.add(wldType.toString());
		
		 }
		 }
	
	private static String statementWriter(List<String> ls, String name ) {
		
		
		
		String result  = ""; 		
		
		for( String temp : ls  ) {
			result += name + " " + "Collected: " + temp + "\n"; 
			
			
		}
		
		
		return  result + name + " Count: " + ls.size() + "\n" 
				+ name + " Term Frequency: " + ls.size()/83.00 + "\n"; 
			
	}
	
	private static class MethodNamePrinter extends VoidVisitorAdapter<Void>{
		
		@Override
		public void visit(MethodDeclaration md, Void arg){
			super.visit(md, arg);
			System.out.println("Method Name Printed NEW: " + md.getName());
		}
	}
	
	private static class MethodNameCollector1 extends VoidVisitorAdapter<List<String>>{
		
		@Override
		public void visit(MethodDeclaration md, List<String> collector){
			super.visit(md, collector);
			collector.add(md.getName().toString());
		}
		
	}
	
	
	//************************************************ATTEMPT TESTS**************************************
	private static final Pattern LOOK_AHEAD_THREE = Pattern.compile("(\\d)(?=(\\d{3})+$)");
	
	 static String formatWithUnderscores(String value){
		 String withoutUnderscores = value.replaceAll("_", ""); 
		 return LOOK_AHEAD_THREE.matcher(withoutUnderscores).replaceAll("$1_"); 
	}
	
	
	private static class IntegerLiteralModifier extends ModifierVisitor<Void>{
		
		@Override
		public FieldDeclaration visit(FieldDeclaration fd, Void arg){
			super.visit(fd, arg);
			
			 fd.getVariables().forEach(v ->
			 		v.getInitializer().ifPresent(i -> {
			 			 if (i instanceof IntegerLiteralExpr) { 
			 			 v.setInitializer(formatWithUnderscores(((IntegerLiteralExpr) i).getValue())); 
			 			 } 
			 		}));	
			return fd;
		}
		
	}
	
	

	
	private static void removeNulls(final List<?> list) {
		for (int i = list.size() - 1; i >= 0; i--) {
			if (list.get(i) == null) {
				list.remove(i);
			}
		}
	}

//************************************************ATTEMPT TESTS**************************************

//*************************************OMAR MODIFIED FOR STATEMENT START****************************************
		private static class FSM extends VoidVisitorAdapter<List<ForStmt>> {
				
			public List<ForStmt> leafNodes = new ArrayList<>();
			
				@Override
				 public void visit(ForStmt fStmt, List<ForStmt> collector) {
				 super.visit(fStmt, collector);
				 
				 	//Prints out the for statement with its body
				 	collector.add(fStmt);
				 	//prints out the init: int i = 2
				 	//	collector.add(test.get(0).toString());
				 	//prints out the comparing i < 100
				 	//	 collector.add(fStmt.getCompare().toString());
				 	//prints out the update factor: i++
				 	//	  collector.add(fStmt.getUpdate().get(0).toString());		 
				 	if(fStmt.getChildNodes().isEmpty()) {
						leafNodes.add(fStmt);
				 	}
				 }
				  public List<ForStmt> getLeafNodes(){
					 return leafNodes; 
				 }
			}

	private static class WSM extends VoidVisitorAdapter<List<WhileStmt>> {
				
			@Override
			public void visit(WhileStmt wStmt, List<WhileStmt> collector) {
			super.visit(wStmt, collector);
				 
				Statement st = JavaParser.parseStatement("int i = 2;");
				 
				 
				 collector.add(wStmt);
			//	 collector.add(wStmt.getBody().toString());
			//	 collector.add(wStmt.getCondition().toString());
			//	wStmt.setBody(st);
			//	collector.add(wStmt.getBody().toString());
			}
	}
			
	private static boolean checkPosition(JavaToken first, JavaToken second) {
		Range firstPos = first.getRange().get();
		Range secondPos = second.getRange().get();
		return firstPos == secondPos;
	}
			   
	 public static void deleteTokenRange(TokenRange range) {
		 JavaToken beginToken = range.getBegin();
		 JavaToken endToken = range.getEnd();

	      //  if (checkPosition(beginToken, endToken)) {
	      //      return;
	      //  }
			   
        /*
        for (JavaToken iter = range.getBegin().getNextToken().get(); !checkPosition(iter, range.getEnd()); iter = iter.getNextToken().get()) {
            iter.deleteToken();
        }
        */
        JavaToken iter = range.getEnd();
        do {
        	iter.deleteToken();
        	iter = iter.getPreviousToken().get();
	        }
        while (iter.getRange().get() != beginToken.getPreviousToken().get().getRange().get());
	 }	 
			 
	  public static void addTokenRange(JavaToken start, TokenRange range) {
	        JavaToken iter = range.getBegin();
	        JavaToken endToken = range.getEnd();

	        while (iter != null) {
	            start.insertAfter(new JavaToken(start.getKind(), start.getText()));
	            if (iter.getNextToken().isPresent() && !checkPosition(iter,endToken)) {
	                iter = iter.getNextToken().get();
	            }
	            else break;
	        }
	  }
			  	
	  public static void deleteInclusiveTokenRange(TokenRange range) {
	        JavaToken beginToken = range.getBegin();
	        JavaToken endToken = range.getEnd();
	        JavaToken iter = beginToken;

	        while (iter != null) {
	            boolean ending = checkPosition(iter, endToken);
	            JavaToken nextToken = iter.getNextToken().get();
	            iter.deleteToken();
	            if (ending) {
	                break;
	            } else {
	                iter = nextToken;
	            }
	        }
	    }
			  
	  public static void insertRangeBefore(JavaToken token, TokenRange range) {
	        JavaToken iter = range.getBegin();
	        JavaToken endToken = range.getEnd();

	        while (iter != null) {
	            JavaToken newToken = new JavaToken(iter.getKind(), iter.getText());
	            //token.insert(newToken);
	            insertBefore(token, newToken);
	            if (iter.getNextToken().isPresent() && !checkPosition(iter,endToken)) {
	                iter = iter.getNextToken().get();
	            }
	            else break;
	        }
	    }
	    // Why they did't update tokens' positions after inserting ?!
	    public static void insertBefore(JavaToken oldToken, JavaToken newToken) {
	        Position oldBegin = oldToken.getRange().get().begin;
	        Position oldEnd = oldToken.getRange().get().end;

	        oldToken.insert(newToken);

	        newToken.setRange(new Range(oldBegin, new Position(oldBegin.line, oldBegin.column + (newToken.asString().length()-1))));

	        if (newToken.getCategory() != EOL) {
	            oldToken.setRange(new Range(new Position(oldBegin.line, oldBegin.column + newToken.asString().length()),
	                    new Position(oldBegin.line,oldEnd.column + newToken.asString().length())));
	        }
	        else {
	            oldToken.setRange(new Range(new Position(oldBegin.line+1,1),
	                    new Position(oldBegin.line+1, oldToken.asString().length())));
	        }
	    }
			    

	    public static void findFirstBrace(TokenRange range, Consumer<JavaToken> action) {
	        JavaToken iter = range.getBegin();
	        while (iter != null && !checkPosition(iter, range.getEnd())) {
	            if (iter.getText().equals("{")) {
	                action.accept(iter);
	                break;
	            }
	            else {
	                if (iter.getNextToken().isPresent()) {
	                    iter = iter.getNextToken().get();
	                } else break;
	            }
	        }
	    }
	    public static JavaToken createEOLToken() {
	        return new JavaToken(GeneratedJavaParserConstants.UNIX_EOL);
	    }
	    public static void insertLines(JavaToken token, int lines, boolean before) {
	        for (int i=0; i<lines; i++) {
	            if (before) {
	                token.insert(createEOLToken());
	            } else {
	                token.insertAfter(createEOLToken());
	            }
	        }
	    }
	    public static void deleteAllRightSpaces(JavaToken iter) {
	        if (iter.getNextToken().isPresent()) {
	            iter = iter.getNextToken().get();

	            while (iter.getCategory() == WHITESPACE_NO_EOL || iter.getCategory() == EOL) {
	                JavaToken nextToken = iter.getNextToken().isPresent()? iter.getNextToken().get(): null;
	                iter.deleteToken();

	                if (nextToken != null) {
	                    iter = nextToken;
	                } else break;
	            }
	        }
	    }
	    public static CompilationUnit FS2WS(CompilationUnit cu){
	    	//Grabbing the attributes of a ForStmt and attaching them in an ArrayList
			List<ForStmt> FLIST = new ArrayList<>();
			VoidVisitor<List<ForStmt>> FSC = new FSM();
			FSC.visit(cu, FLIST);
				
					
			for(int i = 0; FLIST.size() > 0;){
						
			/**
			 * Getting the size to guarantee no indexoutofbounds
			 * deleteAllRightSpaces not to insert the bracket too early
			 * JavaToken here grabbing the last element and checking that it is )
			 * once it is delet all rightspaces again in order not to insert too early
			 * check if { exist if not add it and update the CU and FLIST
			 * otherwise get next token
			 */
			int counter = 0;
			int k =0;
			while(k == 0){
				if(FLIST.get(i).getTokenRange().get().getBegin().getPreviousToken().get().equals(EOL)){
					counter++;
			//		System.out.println("Counter" + counter);
				}else{
					k=1;
			//		System.out.println("Counter" + counter);
						
				}
			}
						
			if(FLIST.get(i).getParentNode().get().getClass().equals(ForStmt.class)){
		
				JavaToken target = FLIST.get(i).getTokenRange().get().getBegin().getPreviousToken().get();
				while(target.getPreviousToken().isPresent()){
					if(target.getText().equals(")")){
						deleteAllRightSpaces(target);
						if(!(target.getNextToken().get().getText().equals("{"))){
							insertBefore(target.getNextToken().get(), new JavaToken(GeneratedJavaParserConstants.LBRACE));
							JavaToken newB = FLIST.get(i).getBody().getTokenRange().get().getEnd().getNextToken().get();
							insertBefore(newB, new JavaToken(GeneratedJavaParserConstants.RBRACE));
							
							cu = JavaParser.parse(cu.getTokenRange().get().toString());
							//Updating the AST and TokenRange
							FLIST = (List<ForStmt>) cu.getChildNodesByType(ForStmt.class);
							break;
						}
					}else{
						if(target.getPreviousToken().isPresent()){
							target = target.getPreviousToken().get();
					}else break;
					}
				}
			}
			else{
				int size = FLIST.get(i).getUpdate().size()-1;
				if(FLIST.get(i).getUpdate().isNonEmpty()){
					deleteAllRightSpaces(FLIST.get(i).getUpdate().get(size).getTokenRange().get().getEnd());
					JavaToken here = FLIST.get(i).getUpdate().get(size).getTokenRange().get().getEnd().getNextToken().get();
					if(here.getText().equals(")")){
						deleteAllRightSpaces(here);
						if(!(here.getNextToken().get().getText().equals("{"))){
							insertBefore(here.getNextToken().get(), new JavaToken(GeneratedJavaParserConstants.LBRACE));
							JavaToken newB = FLIST.get(i).getBody().getTokenRange().get().getEnd().getNextToken().get();
							insertBefore(newB, new JavaToken(GeneratedJavaParserConstants.RBRACE));
							
							cu = JavaParser.parse(cu.getTokenRange().get().toString());
							//Updating the AST and TokenRange
							FLIST = (List<ForStmt>) cu.getChildNodesByType(ForStmt.class);
							continue;
						}
					}else{
						if(here.getNextToken().isPresent()){
							here = here.getNextToken().get();
						}else break;
					}
				}
			}
				
					
				//getting the elements inside the body of the For-Statement
				List<Node> bodyList = (List<Node>) FLIST.get(i).getBody().getChildNodes();
				int ii = bodyList.size() - 1;
				Node lastStm =  bodyList.get(ii);
				//while(!(lastStm.isAssignableFrom(Statement.class)) && i >= 0 ) {
				while(!(lastStm instanceof Statement) && ii >= 0 ) {
					lastStm = bodyList.get(ii);
					ii --;
				}
				JavaToken first;
				if(FLIST.get(i).getParentNode().get().getClass().equals(LabeledStmt.class) 
					|| FLIST.get(i).getParentNode().get().getClass().equals(IfStmt.class)
					|| FLIST.get(i).getParentNode().get().getClass().equals(ForeachStmt.class)){
					first = FLIST.get(i).getParentNode().get().getTokenRange().get().getBegin().getPreviousToken().get();
				}else{
					first = FLIST.get(i).getTokenRange().get().getBegin().getPreviousToken().get();
				}
				JavaToken last = lastStm.getTokenRange().get().getEnd().getNextToken().get();
					
					
				TokenRange initRange;
				//inserting the initialization before the while statement; adding a semicolon; ending the line
				if(FLIST.get(i).getInitialization().isNonEmpty()){
					for(int j = 0;j<FLIST.get(i).getInitialization().size();j++){
						initRange = FLIST.get(i).getInitialization().get(j).getTokenRange().get();
						insertRangeBefore(first, initRange);
						insertBefore(first, new JavaToken(GeneratedJavaParserConstants.SEMICOLON));
						insertBefore(first , new JavaToken(GeneratedJavaParserConstants.UNIX_EOL));
					}
				}
				
				
			TokenRange updateRange;
			if(FLIST.get(i).getUpdate().isNonEmpty()){
				for(int j=0;j<FLIST.get(i).getUpdate().size();j++){
					//inserting the update statement; adding a semicolon
					updateRange = FLIST.get(i).getUpdate().get(j).getTokenRange().get();
					insertRangeBefore(last, updateRange);
					insertBefore(last, new JavaToken(GeneratedJavaParserConstants.SEMICOLON));
					insertBefore(last , new JavaToken(GeneratedJavaParserConstants.UNIX_EOL));
				}
			}
			
			//assigning the body of the For-Statement to a temp variable to insert it in the While-Statement
			Statement newBody = JavaParser.parseStatement(FLIST.get(i).getBody().getTokenRange().get().toString());
			//Constructing the While-Statement
			Statement st1;
			if(FLIST.get(i).getCompare().isPresent()){
				st1 = JavaParser.parseStatement("while(" + FLIST.get(i).getCompare().get() + ") " + newBody );
				
			}else{
				st1 = JavaParser.parseStatement("while(" + true + ") " + newBody );
			}
					
			/**
			 * 1) fstmtrange: represents where the For-Statement exist within the code. ex, line 10 - line 14
			 * 2) startToken: the start of the For-Statement line. Ex, For(int i=0;i<100;i++){}  startToken = F but we grab previous
			 * 3)insertRangeBefore();  we insert the While-Statement in that location
			 * 4) deleteInclusiveTokenRange(); deleting the For-Statement
			 */
					
			TokenRange fstmtrange = FLIST.get(i).getTokenRange().get();	
			JavaToken startToken = fstmtrange.getBegin().getPreviousToken().get();		
			insertRangeBefore(startToken ,st1.getTokenRange().get());
			deleteInclusiveTokenRange(fstmtrange);
				
					
		//	System.out.println("CU: " + cu.getTokenRange().get().toString());
			cu = JavaParser.parse(cu.getTokenRange().get().toString());
			//Updating the AST and TokenRange
			FLIST = (List<ForStmt>) cu.getChildNodesByType(ForStmt.class);
			}
		///	System.out.println("RETURN: " + cu.toString());
	    return cu;
	    }
			    
	    public static CompilationUnit WS2FS(CompilationUnit cu){
			//Grabbing the attributes of a WStmt and attaching them in an ArrayList
			List<WhileStmt> WLIST = new ArrayList<>();
			VoidVisitor<List<WhileStmt>> WSC = new WSM();
			WSC.visit(cu,  WLIST);
			
			VariableDeclarator temp;
				
			for(int i = 0; WLIST.size()>0;){
				int size = WLIST.get(i).getBody().getChildNodes().size();
					
				typeSolver = new CombinedTypeSolver();
					
				//grabbing the compare TokenRange
				TokenRange compare = WLIST.get(i).getCondition().getTokenRange().get();
					
				//assigning the body of the While-Statement to a temp cariable to isnert it in the For-Statement
				Statement newBody = JavaParser.parseStatement(WLIST.get(i).getBody().getTokenRange().get().toString());
				//constructing the For-Statement
				Statement st1 = JavaParser.parseStatement("for( ;" + compare + ";) " + newBody);
					
					
				/**
				 * 1) wstmtrange: represents where the While-Statement exist within the code. ex, line 10 - line 14
				 * 2) startToken: the start of the While-Statement line. Ex, For(int i=0;i<100;i++){}  startToken = F but we grab previous
				 * 3)insertRangeBefore();  we insert the While-Statement in that location
				 * 4) deleteInclusiveTokenRange(); deleting the While-Statement
				 */
					
				TokenRange wstmtrange = WLIST.get(i).getTokenRange().get();
				JavaToken startToken = wstmtrange.getBegin().getPreviousToken().get();
				insertRangeBefore(startToken, st1.getTokenRange().get());
				deleteInclusiveTokenRange(wstmtrange);	
				//	System.out.println("========================================================= : " + i + WLIST.get(i));
				//	System.out.println("Before: " + cu);
				cu = JavaParser.parse(cu.getTokenRange().get().toString());
				//Updating the AST and TokenRange
				//		System.out.println("AFTER: " + cu);
				WLIST = (List<WhileStmt>) cu.getChildNodesByType(WhileStmt.class);
			}
			return cu;
	    }
			    
	    public static Expression Int2Exp(int n){		    	
	    	Expression temp = JavaParser.parseExpression(Integer.toString(n));
	    	return temp;
	    }
	    public static int loopCounter;
	    public static SwitchStmt addCase(int n, SwitchStmt ss, List<Statement> body, int stage){			    	
	    	SwitchEntryStmt temp;    	
	    	swVarCounter++;
	    	Statement brk = JavaParser.parseStatement("break;");;
	    	Statement swVar =  JavaParser.parseStatement("swVar = " + swVarCounter + ";");
	    	Statement helperTR;
			    	
	    	TokenRange swVarTR = swVar.getTokenRange().get();;
	    	JavaToken location;

	    	IfStmt ifHelper;

	    	Statement swVarExit = JavaParser.parseStatement("swVar = " + 0 + ";");
		    //	Statement swVarReturn = JavaParser.parseStatement("swVar = " + --swVarCounter + ";");
			    	
	    	Statement constructIf;
	    	Statement ifSt ;
	    	Statement elseSt;
	    	List<Statement> tempList = new ArrayList<>();
			    	
	    	int exitCounter = 0;
			    	
			    	
	    	if(stage == 0){
	    		//INIT STAGE
			    		
	    			body.add(swVar);
	    			body.add(brk);
			    	temp = new SwitchEntryStmt(Int2Exp(n), (NodeList<Statement>) body);
			    	ss.addEntry(temp);
			    			
			    		
	    	}else if(stage == 1){
			    		
			    		
	    		location = body.get(0).getTokenRange().get().getEnd();
	    		insertRangeBefore(location, swVarTR);
	    		helperTR = JavaParser.parseStatement(body.get(0).getTokenRange().get().toString());
	    		body.set(0, helperTR);
		    		
	    		ifHelper = (IfStmt)body.get(0);
	    		ifHelper.setElseStmt(swVarExit);
			    		
	    		body.add(brk);
	    		temp = new SwitchEntryStmt(Int2Exp(n), (NodeList<Statement>) body);
	    		ss.addEntry(temp);
	    		loopCounter = swVarCounter-1;
			    		
	    	}else if(stage == 2){
	    		Statement loop = JavaParser.parseStatement("swVar = "+ loopCounter + ";");
		    		
	    		body.add(loop);
	    		body.add(brk);
	    		temp = new SwitchEntryStmt(Int2Exp(n), (NodeList<Statement>) body);
	    		ss.addEntry(temp);
			    		
			    		
			    		
	    	}else{
			    	
			    	
	    		for(int i = 0; i < body.size();i++){
			   // 		System.out.println("Element number: " + i + ", : " + body.get(i) + " : " + body.get(i).getClass().getSimpleName());
			   // 		System.out.println("LOCATION: " + body.get(i).getTokenRange().get().getEnd());
			    		
	    		if(body.get(i).getClass().getSimpleName().equals("IfStmt")){
		    	//		System.out.println("We have entered the ifStmt section");
		    	//		System.out.println("Encountered an IfStmt: " + body.get(i));
	    			location = body.get(i).getTokenRange().get().getEnd();
	    			insertRangeBefore(location, swVarTR);
			    			
	    			helperTR = JavaParser.parseStatement(body.get(i).getTokenRange().get().toString());
	    			body.set(i, helperTR);
			    				
	    			ifHelper = (IfStmt)body.get(i);
	    			ifHelper.setElseStmt(swVarExit);
    				exitCounter = swVarCounter;
		    		//		System.out.println("ELEMENT AFTER: " + i + ", : " + body.get(i) + " : CLASS: " + body.get(i).getClass().getSimpleName());
	    			break;
	    		}else{
		    		//	System.out.println("We have entered the elseStmt");
	    			if(body.get(i).getClass().getSimpleName().equals("IfStmt")){
			    	//			System.out.println("CAUGHT");
	    			}else{
			    			
		    			body.add(swVar);
		    			break;
	    			}
	    		}
			    	
	    	}
			    	
			    	
    	}			    				    	
    	return ss;
    }
	    
    public static String getSaltString() {
        String SALTCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        StringBuilder salt = new StringBuilder();
        Random rnd = new Random();
        while (salt.length() < 18) { // length of the random string.
            int index = (int) (rnd.nextFloat() * SALTCHARS.length());
            salt.append(SALTCHARS.charAt(index));
        }
        String saltStr = salt.toString();
        return saltStr;
    }
			    
			    
    public static List<Statement> neInitList = new ArrayList<>();
    public static List<Statement> neInitListConvert = new NodeList<>();
    public static List<Statement> cleanInitList = new NodeList<>();
			    
    public static void transformOmar(ForStmt fs){
    	//OMAR CODE
    	// NameExpr Visitor
    	// for(int i=0;i<temp.size();i++){
       	// System.out.println("THIS IS THE ZERO: " + temp.get(i));
			    	
    	//List<ForStmt> temp = cu.getChildNodesByType(ForStmt.class);
    		new VoidVisitorAdapter<Void>() {
    			@Override public void visit(NameExpr n, Void arg) {
			   	            	
    				Node temp = n.getParentNode().get().getParentNode().get();	            	
			   	            		
			   	            	
    				buildVarMapOm(n, "nEXP");
			   	            	
    			}
    	}.visit(fs, null);
    }
    public static void buildVarMapOm(Node node, String type){
		//    	List<Statement> rtrnStmt = new NodeList();

    	if(node instanceof NameExpr){
        	int counter = 1;
            Node temp = node;
            Node helper = null;
            int STEPONE = 1;   //STEPONE is looping to get the first BlockStmt
            int STEPTWO = 1;  // STEPTWO is looping to search for a match to our node
            int RESET = 0;  //RESET THE  Z VALUE
		  //              System.out.println("========================= The Node: " + node + " ======================");
            while(STEPONE == 1){
            	//keep getting the ParentNode until we reach the full BlockStmt
            	if(temp.getClass().getSimpleName().equals("BlockStmt")){
            		// node is the first BlockStmt here for that node
            		//		System.out.println("We have reached the BockStmt" + temp);	
            		for(int z = 0; z < temp.getChildNodes().size(); z++){
            			if(RESET == 0){
                			helper = temp.getChildNodes().get(z);
            			}else{
            				RESET = 0;
            				z = 0;
            				helper = temp.getChildNodes().get(z);
			                			}
            				while(STEPTWO == 1){
	                			//temp will be the childnodes of the BlockStmt where each Expression is .get(0) .get(1) ... 
	                			if(helper.getClass().getSimpleName().equals("AssignExpr")){
	                				//		System.out.println("Reached AssignExpr: " + helper);
	                				for(int q = 0; q < helper.getChildNodes().size(); q++){
		                					if(helper.getChildNodes().get(q).equals(node)){
		                				//		System.out.println(node + ", FOUND ITS EXPRESSIONO: " + helper);
		                				//		rtrnStmt.add((Statement)helper.getParentNode().get());
		                						
		                						neInitList.add((Statement)helper.getParentNode().get());
		                						STEPTWO = 0;
		                						break;
		                					}else{
			                	//					System.out.println(node + ", Not a Match: " + helper);
		                					}
	                				}           				
			                				break;
	                			}else if(helper.getClass().getSimpleName().equals("VariableDeclarationExpr")){
	                		//		System.out.println("Reached VariableDeclarationExpr");
	                				//needed the VariableDeclarationExpr because it goes down another level
	                				//break down the childnodes into simplename isntead of nameExpr because AST
	                				//from here is different, final level is simplename.class
	                				for(int k = 0; k < helper.getChildNodes().size(); k++){
	                					if(helper.getChildNodes().get(k).getTokenRange().get().getBegin().equals(node.getTokenRange().get().getBegin())){
	                						//System.out.println(node + ", Found its VariableDeclarationExpr: " + helper.getChildNodes().get(0));
	                				//		rtrnStmt.add((Statement)helper.getParentNode().get());
	                						Statement fix = JavaParser.parseStatement(helper.getChildNodes().get(0) +  ";");
	                						neInitList.add(fix);
	                						STEPTWO = 0;
	                					}else{
	                						
	                						helper = temp.getChildNodes().get(k);
	                					}
	                				}
	                				break;
	                			}else 
	                				//if(helper.getClass().getSimpleName().equals("SimpleName") || helper.getClass().getSimpleName().equals("NameExpr")
	                				//	|| helper.getClass().getSimpleName().equals("BooleanLiteralExpr") || helper.getClass().getSimpleName().equals("IntegerLiteralExpr")
	                				//	|| helper.getClass().getSimpleName().equals("BreakStmt") || helper.getClass().getSimpleName().equals("LineComment")
	                				//	|| helper.getClass().getSimpleName().equals("StringLiteralExpr")){
	                				if(helper.getChildNodes().isEmpty()){
	                				//		System.out.println("Reached SimpleName: " + helper);
	                		//		System.out.println("TEMP IN SIMPLENAME: " + temp + ", CLASS: " + temp.getClass().getSimpleName());
	                		//		System.out.println("Temp ParentNode: " + temp.getParentNode().get() + ", CLASS: " + temp.getParentNode().get().getClass().getSimpleName());
	                				String dad = temp.getParentNode().get().getClass().getSimpleName();
	                				if(dad.equals("IfStmt") || dad.equals("WhileStmt") || dad.equals("ForStmt") || dad.equals("ForeachStmt")){
	                		//			System.out.println("HOWWWW: "  + temp);
	                					temp = temp.getParentNode().get().getParentNode().get();	
	                		//			System.out.println("HOWWWWWWWWWW: " + temp);
	                					z = 0;
	                		//			System.out.println("WOW REALLY? " + helper);
	                					helper = temp.getChildNodes().get(z);
	                		//			System.out.println("really....." + helper);
	                					RESET = 1;
	                				}
	                				break;
	                			}else{
	                				//this else keeps getting the childNode till we hit one of them
	                		//		System.out.println("HELPER HERE: " + helper);
	                				System.out.println("HELPER: "  + helper + ": : " + helper.getClass().getSimpleName());
	                				
	                				helper = helper.getChildNodes().get(0);
	                		//		System.out.println("HELPER HERE: " + helper);
	                			//	System.out.println("Temp BLock: " + temp);
	            //    				System.out.println("CURRENT: " + helper + ", CLASS: " + helper.getClass().getSimpleName());
                				//	if(temp.getClass().getSimpleName().equals("SimpleName"))
	                			}
	                		}
			                
                		}
                		STEPONE = 0;
                	}else{
                		//getting the BlockStmt
                		temp = temp.getParentNode().get();
                		if(!(temp.getClass().getSimpleName().equals("BlockStmt"))){
                			temp = temp.getParentNode().get();
                		}
                	}           	
                }          	
        	}else{
  //      		System.out.println("Not a nameExpression");
        	}
//	    	System.out.println("The ReturnStmt: " + rtrnStmt);
	//      return rtrnStmt;
    } 
    
		
    public static NodeList<Statement> convertAL2NL(ArrayList<Statement> aList){
    	//This method is needed because when we deal with SwitchEntryStmt
    	//We need NodeList instead of ArrayList
		//If you make something work for ArrayList, high chance it will not work for NodeList which is needed
    	//instead use this method to just convert at the end because ArrayList is easier
    	List<Statement> temp = new NodeList<>();
    	for(int i = 0; i < aList.size(); i++){
    		temp.add(aList.get(i));
    	}
    	return (NodeList<Statement>) temp;
    }
		    
    public static List<Statement> safeKeeping = new ArrayList<>();
    public static CompilationUnit switchOBFS(CompilationUnit cu){  	
	    	
    	//Highly recommend to turn all the ForStmt into WhileStmt and then back to ForStmt
    	//only issue have to deal with duplicate initializations but the obfuscation would be really nice
    //	System.out.println("ONE: " + cu);
    	cu = FS2WS(cu);
    //	System.out.println("TWO: " + cu);
    	cu = WS2FS(cu);
		System.out.println("Three: =========================================" + cu + "========================END");
		//Scannign the CompilationUnit, collecting the ForStmt and attaching them in an ArrayList
		List<ForStmt> FLIST = new ArrayList<>();
		VoidVisitor<List<ForStmt>> FSC = new FSM();
		FSC.visit(cu, FLIST);
		
	//	System.out.println();
		
		
		VariableDeclarationExpr expstm = JavaParser.parseVariableDeclarationExpr("int swVar = 1");
		TokenRange expstmTR = expstm.getTokenRange().get();
		JavaToken fFix;
		boolean once = false;
		
		
		while(!once){
			for(int w = 0; w < cu.getChildNodes().size(); w++){
				if(cu.getChildNodes().get(w).getClass().getSimpleName().equals("ClassOrInterfaceDeclaration")){
					for(int r = 0; r < cu.getChildNodes().get(w).getChildNodes().size(); r++){
						if(cu.getChildNodes().get(w).getChildNodes().get(r).getClass().getSimpleName().equals("MethodDeclaration")){
							int size = cu.getChildNodes().get(w).getChildNodes().get(r).getChildNodes().size();
							fFix = cu.getChildNodes().get(w).getChildNodes().get(r).getChildNodes().get(size-1).getChildNodes().get(0).getTokenRange().get().getBegin();
							insertRangeBefore(fFix, expstmTR);
							insertBefore(fFix, new JavaToken(GeneratedJavaParserConstants.SEMICOLON));
							insertBefore(fFix , new JavaToken(GeneratedJavaParserConstants.UNIX_EOL));
							once = true;
						}
						
					}
				}
			}
		}
		
		//Main Loop for each ForStmt
		for(int i = 0; FLIST.size() > 0;){
			
			//first : grabs the begining of the ForStmt as a JavaToken, controls where to input new code
			JavaToken first;
			
			//When we can't use nodes we have to use TokenRange
			TokenRange swVar = expstm.getTokenRange().get();
					
			SwitchStmt swVarSwitch = (SwitchStmt) JavaParser.parseStatement("switch(swVar){}");
			//When we can't use nodes we have to use TokenRange
			TokenRange swVarSwitchTR = swVarSwitch.getTokenRange().get();
					
			Node tmp = FLIST.get(i).getParentNode().get();
			List<Statement> tmpL = new ArrayList<>();
			

			boolean flagParent = false;
			while(!flagParent){
				if(tmp.getClass().getSimpleName().equals("ForStmt")){
				//	System.out.println("Reached it: "   + tmp);
					flagParent = true;
					break;
				}else{
					if(tmp.getParentNode().isPresent())
						tmp = tmp.getParentNode().get();
					else
						break;
				}
			}
			//System.out.println("FLAGGGGGG: " + flagParent);
			
			//The output is stored in a ArrayList called: neInitList
			//Collects the NameExpr in the ForStmt
			transformOmar(FLIST.get(i));	
			
			
			
		//	System.out.println("BEFORE: " + neInitList);
			
			//Eliminating duplicate init in the list
			if(neInitList.size() > 1){
				for(int y = 0; y < neInitList.size(); y++){
					for(int j = y+1; j < neInitList.size(); j++){
						if(neInitList.get(y).equals(neInitList.get(j))){
							neInitList.remove(j);
						}
					}
				}
		
			}
		
			if(flagParent){
				for(int k = 0; k < neInitList.size(); k++){
					safeKeeping.add(neInitList.get(k));
				}
			}
		//	System.out.println("SAFE: " + safeKeeping);
		//	System.out.println("ORIGIN BEFORE: " + neInitList);
			//Eliminating duplicate init in the list because of scope
			if(neInitList.size() > 1){
				for(int y = 0; y < safeKeeping.size(); y++){
			//		System.out.println("SIZE IN LOOP: " + neInitList.size());
					for(int j = 0; j < neInitList.size(); j++){
		//				System.out.println("Checking: " + neInitList.get(j));
						if(safeKeeping.get(y).equals(neInitList.get(j)) ){
							neInitList.remove(j);		
						}
					}
				}
			}
			
	//		System.out.println("Origin AFter: " + neInitList);
			
			
					
			//Converting to a NodeList in order to be able interact with the Switch
			neInitListConvert = convertAL2NL((ArrayList<Statement>) neInitList);
			//First addCase for case1: initializing the NameExpression
			addCase(caseCounter++, swVarSwitch, neInitListConvert, 0);
			
			//Eliminating duplicate init in the list
			if(neInitList.size() > 1){
				for(int y = 0; y < neInitList.size(); y++){
					for(int j = y+1; j < neInitList.size(); j++){
						if(neInitList.get(y).equals(neInitList.get(j))){
							neInitList.remove(j);
						}
					}
				}
			}
					
			List<Statement> tempStmt = new ArrayList<>();
			Statement ifHelper = null;
			List<Statement> childTempStmt = new ArrayList<>();
					
			ifHelper = JavaParser.parseStatement( "if(" + FLIST.get(i).getCompare().get().toString() + "){}");
			tempStmt.add(ifHelper);
					
			//Second addCase for case2: having the compare in an IF and exit else
			addCase(caseCounter++, swVarSwitch, convertAL2NL((ArrayList<Statement>) tempStmt), 1);
					
			//Grabbing the secondChildNode because the first one is the compare and that one was handled above
			List<Node> temp = null;
			//start at 1 because 0 was the compare and we completed that above
			if(FLIST.get(i).getChildNodes().get(1) != null)
				temp = FLIST.get(i).getChildNodes().get(1).getChildNodes();
		
				for(int j = 0; j < temp.size(); j++){
			//		System.out.println("Child Number: " + j + ", : " + temp.get(j) + ", CLASS: " + temp.get(j).getClass().getSimpleName());
					System.out.println("HERE: " + temp.get(j) + " ::: " + temp.get(j).getClass().getSimpleName());
					childTempStmt.add((Statement)temp.get(j));
				}
				//Third addCase for case3: having the childNode in this one
				addCase(caseCounter++, swVarSwitch, convertAL2NL((ArrayList<Statement>)childTempStmt), 2);
					
				
				
				//have to construct the Switch fully before feeding it into the WhileStmt 
				
				WhileStmt swVarWhile = (WhileStmt)JavaParser.parseStatement("while(swVar != 0){ \n\t" + swVarSwitch + "\n}");
				TokenRange swVarWhileTR = swVarWhile.getTokenRange().get();
				int numberOfStmt = 0; 
				
						
				TokenRange fstmtrange = FLIST.get(i).getTokenRange().get();
				//first represents the first forloop and we are inserting the SwitchVariable behind it
				
				first = FLIST.get(i).getTokenRange().get().getBegin();
					
					
			//	insertRangeBefore(first, swVar);
			//	insertBefore(first, new JavaToken(GeneratedJavaParserConstants.SEMICOLON));
			//	insertBefore(first , new JavaToken(GeneratedJavaParserConstants.UNIX_EOL));
				
				System.out.println("BEFORE DISASTER: " + cu.getTokenRange().get());
				//inserting  the WhileStmt + SwitchStmt before the For and after the SwitchVariable
				
				insertRangeBefore(first, swVarWhileTR);
				insertBefore(first , new JavaToken(GeneratedJavaParserConstants.UNIX_EOL));
				deleteInclusiveTokenRange(fstmtrange);
					
				//CLR() ; to clear the values not to overwrise because the need of global variables
				CLR();
				System.out.println("THIS ONE? " + cu.getTokenRange().get());
				cu = JavaParser.parse(cu.getTokenRange().get().toString());
				FLIST = (List<ForStmt>) cu.getChildNodesByType(ForStmt.class);
				
			}	
    	return cu;
    }
			    
    public static void CLR(){
    	swVarCounter = 1;
    	caseCounter = 1;
    	neInitList.clear();		    	
    }
    
    public static CombinedTypeSolver typeSolver;
    public static int caseCounter = 1;
	public static Statement NELIST = null;
    public static int swVarCounter = 1;
	   
	public static void main(String[] args) throws Exception {
		
		try 
				
				 {
			
			
			ArrayList<Path> fileList = new ArrayList<>(); 
			String filepath = "\\Users\\omar1\\Desktop\\DataSet"; 
			Path source = Paths.get(filepath); 
			Files.walk(source).filter(p -> p.toString().endsWith(".java")).forEach(fileList::add); 
		
			
			for (Path javaFile : fileList )  {
					
				String jfile = javaFile.toString().replace(".java", ".txt"); 
				String jfilej2 = javaFile.toString().replace(".java", ".java2");
				
				File newJavaFile = new File(jfile); 
		
				
				FileWriter fwriter = new FileWriter(newJavaFile); 
				FileWriter fwriter1 = new FileWriter(new File(jfilej2));
						
				BufferedWriter writer = new BufferedWriter(fwriter);
				BufferedWriter writer1 = new BufferedWriter(fwriter1);

		
				 leafMap.clear(); 
				
			
				
				
			
	
			
		 
		{
			
			
		 
		
		
		CompilationUnit cu = JavaParser.parse(new FileInputStream(javaFile.toString()));
		
		
	
		cu = switchOBFS(cu);
		writer1.write(cu.getTokenRange().toString());
	//	writer1.write(FS2WS(cu).getTokenRange().get().toString());
		//writer1.write(WS2FS(cu).getTokenRange().get().toString());
		
		
		/*prints out node types and count
	 	term frequency is calculated by dividing the count of a node type by the number of different types of nodes (83)
	 	-could also divide by number of different nodes in particular file					*/
		
		
		
		List<String> annotationNames = new ArrayList<>();
		VoidVisitor<List<String>> annotationNameVisitor = new AnnotationCollector();
		annotationNameVisitor.visit(cu, annotationNames);
		annotationNames.forEach(n -> System.out.println("Annotation Collected: " + n));
		System.out.println("Annotation Count: " + annotationNames.size());
		writer.write(statementWriter(annotationNames, "Annotation" ));
		
		List<String> annotationMemberNames = new ArrayList<>();
		VoidVisitor<List<String>> annotationMemberNameVisitor = new AnnotationMemberCollector();
		annotationMemberNameVisitor.visit(cu, annotationMemberNames);
		annotationMemberNames.forEach(n -> System.out.println("Annotation Member Collected: " + n));
		System.out.println("Annotation Member Count: " + annotationMemberNames.size()); 		
		
		writer.write(statementWriter(annotationMemberNames, "Annotation Member" ));
		
		List<String> arrayAccessExprNames = new ArrayList<>();
		VoidVisitor<List<String>> arrayAccessExprNameVisitor = new ArrayAccessExprCollector();
		arrayAccessExprNameVisitor.visit(cu, arrayAccessExprNames);
		System.out.println(arrayAccessExprNames);
		arrayAccessExprNames.forEach(n -> System.out.println("Array Access Expression Collected: " + n));
		System.out.println("Array Access Expression Count: " + arrayAccessExprNames.size()); 
		writer.write(statementWriter(arrayAccessExprNames, "Array Access Expression" ));
		
		List<String> arrayCreationExprNames = new ArrayList<>();
		VoidVisitor<List<String>> arrayCreationExprNameVisitor = new ArrayCreationExprCollector();
		arrayCreationExprNameVisitor.visit(cu, arrayCreationExprNames);
		arrayCreationExprNames.forEach(n -> System.out.println("Array Creation Expression Collected: " + n));
		System.out.println("Array Creation Expression Count: " + arrayCreationExprNames.size()); 
		writer.write(statementWriter(arrayCreationExprNames, "Array Creation Expression" ));
			  
		List<String> arrayCreationLevelNames = new ArrayList<>();
		VoidVisitor<List<String>> arrayCreationLevelNameVisitor = new ArrayCreationLevelCollector();
		arrayCreationLevelNameVisitor.visit(cu, arrayCreationLevelNames);
		arrayCreationLevelNames.forEach(n -> System.out.println("Array Creation Level Collected: " + n));
		System.out.println("Array Creation Level Count: " + arrayCreationLevelNames.size()); 
		writer.write(statementWriter(arrayCreationLevelNames, "Array Creation Level" ));
		
		
		List<String> arrayInitializerNames = new ArrayList<>();
		VoidVisitor<List<String>> arrayInitializerNameVisitor = new ArrayInitializerExprCollector();
		arrayInitializerNameVisitor.visit(cu, arrayInitializerNames);
		arrayInitializerNames.forEach(n -> System.out.println("Array Initializer Collected: " + n));
		System.out.println("Array Initializer Count: " + arrayInitializerNames.size()); 
		writer.write(statementWriter(arrayInitializerNames, "Array Initializer" ));
		
		List<String> arrayTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> arrayTypeNameVisitor = new ArrayTypeCollector();
		arrayTypeNameVisitor.visit(cu, arrayTypeNames);
		arrayTypeNames.forEach(n -> System.out.println("Array Type Collected: " + n));
		System.out.println("Array Type Count: " + arrayTypeNames.size()); 
		writer.write(statementWriter(arrayInitializerNames, "Array Type" ));
		
		List<String> assertStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> assertStmtNameVisitor = new AssertStmtCollector();
		assertStmtNameVisitor.visit(cu, assertStmtNames);
		assertStmtNames.forEach(n -> System.out.println("Assert Statment Collected: " + n));
		System.out.println("Assert Statment Count: " + assertStmtNames.size());
		writer.write(statementWriter(assertStmtNames, "Assert Statment" ));
		
		List<String> assignExprNames = new ArrayList<>();
		VoidVisitor<List<String>> assignExprNameVisitor = new AssignExprCollector();
		assignExprNameVisitor.visit(cu, assignExprNames);
		System.out.println(assignExprNames);
		assignExprNames.forEach(n -> System.out.println("Assign Expression Collected: " + n));
		System.out.println("Assign Expression Count: " + assignExprNames.size());
		writer.write(statementWriter(assignExprNames, "Assign Expression" ));
		
		
		List<String> binaryExprNames = new ArrayList<>();
		VoidVisitor<List<String>> BinaryExprNameVisitor = new BinaryExprCollector();
		BinaryExprNameVisitor.visit(cu, binaryExprNames);
		binaryExprNames.forEach(n -> System.out.println("Binary Expression Collected: " + n));
		System.out.println("Binary Expression Count: " + binaryExprNames.size());
		writer.write(statementWriter(binaryExprNames, "Binary Expression" ));
		
		List<String> blockCommentNames = new ArrayList<>();
		VoidVisitor<List<String>> blockCommentNameVisitor = new BlockCommentCollector();
		blockCommentNameVisitor.visit(cu, blockCommentNames);
		blockCommentNames.forEach(n -> System.out.println("Block Comment Collected: " + n));
		System.out.println("Block Comment Count: " + blockCommentNames.size());
		writer.write(statementWriter(blockCommentNames, "Block Comment" ));
		
		List<String> blockStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> blockStmtNameVisitor = new BlockStmtCollector();
		blockStmtNameVisitor.visit(cu, blockStmtNames);
		blockStmtNames.forEach(n -> System.out.println("Block Statement Collected: " + n));
		System.out.println("Block Statement Count: " + blockStmtNames.size());		
		writer.write(statementWriter(blockStmtNames, "Block Statement" ));
		
		List<String> booleanLitExprNames = new ArrayList<>();
		VoidVisitor<List<String>> booleanLitExprNameVisitor = new BooleanLiteralExprCollector();
		booleanLitExprNameVisitor.visit(cu, booleanLitExprNames);
		booleanLitExprNames.forEach(n -> System.out.println("Boolean Literal Expression Collected: " + n));
		System.out.println("Boolean Literal Expression Count: " + booleanLitExprNames.size());		
		writer.write(statementWriter(booleanLitExprNames, "Boolean Literal Expression" ));
		
		List<String> breakStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> breakStmtNameVisitor = new BreakStmtCollector();
		breakStmtNameVisitor.visit(cu, breakStmtNames);
		breakStmtNames.forEach(n -> System.out.println("Break Statement Collected: " + n));
		System.out.println("Break Statement Count: " + breakStmtNames.size());	
		writer.write(statementWriter(breakStmtNames, "Break Statement" ));
		
		List<String> castExprNames = new ArrayList<>();
		VoidVisitor<List<String>> castExprNameVisitor = new CastExprCollector();
		castExprNameVisitor.visit(cu, castExprNames);
		castExprNames.forEach(n -> System.out.println("Cast Expression Collected: " + n));
		System.out.println("Cast Expression Count: " + castExprNames.size());
		writer.write(statementWriter(castExprNames, "Cast Expression" ));
		
		List<String> catchClauseNames = new ArrayList<>();
		VoidVisitor<List<String>> catchClauseNameVisitor = new CatchClauseCollector();
		catchClauseNameVisitor.visit(cu, catchClauseNames);
		catchClauseNames.forEach(n -> System.out.println("Catch Clause Collected: " + n));
		System.out.println("Catch Clause Count: " + catchClauseNames.size());
		writer.write(statementWriter(catchClauseNames, "Catch Clause" ));
		
		List<String> charLiteralExprNames = new ArrayList<>();
		VoidVisitor<List<String>> charLiteralExprNameVisitor = new CharLiteralExprCollector();
		charLiteralExprNameVisitor.visit(cu, charLiteralExprNames);
		charLiteralExprNames.forEach(n -> System.out.println("Char Literal Expression Collected: " + n));
		System.out.println("Char Literal Expression Count: " + charLiteralExprNames.size());
		writer.write(statementWriter(charLiteralExprNames, "Char Literal Expression" ));
		
		List<String> classExprNames = new ArrayList<>();
		VoidVisitor<List<String>> classExprNameVisitor = new ClassExprCollector();
		classExprNameVisitor.visit(cu, classExprNames);
		classExprNames.forEach(n -> System.out.println("Class Expression Collected: " + n));
		System.out.println("Class Expression Count: " + classExprNames.size());
		writer.write(statementWriter(classExprNames, "Class Expression" ));
		
		//switch to <string>?  
		List<String> classOrInterfaceNames = new ArrayList<>();
		VoidVisitor<List<String>> classOrInterfaceNameCollector = new ClassOrInterfaceDeclarationCollector();
		classOrInterfaceNameCollector.visit(cu, classOrInterfaceNames);
		classOrInterfaceNames.forEach(n -> System.out.println("Class or Interface Collected: " + n));
		System.out.println("Class or Interface Count: " + classOrInterfaceNames.size());
		writer.write(statementWriter(classOrInterfaceNames, "Class or Interface" ));
		
		
		
		List<String> classOrInterfaceTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> classOrInterfaceTypeNameVisitor = new ClassOrInterfaceTypeCollector();
		classOrInterfaceTypeNameVisitor.visit(cu, classOrInterfaceTypeNames);
		classOrInterfaceTypeNames.forEach(n -> System.out.println("Class or Interface Type Collected: " + n));
		System.out.println("Class or Interface Type Count: " + classOrInterfaceTypeNames.size());
		writer.write(statementWriter(classOrInterfaceTypeNames, "Class or Interface Type" ));
		
		//prints out program...look for a shorter way to print
		List<String> compilationUnitNames = new ArrayList<>();
		VoidVisitor<List<String>> compilationUnitNameVisitor = new CompilationUnitCollector();
		compilationUnitNameVisitor.visit(cu, compilationUnitNames);
		compilationUnitNames.forEach(n -> System.out.println("Compilation Unit Collected: " + n));
		System.out.println("Compilation Unit Count: " + compilationUnitNames.size());
		writer.write(statementWriter(compilationUnitNames, "Compilation Unit" ));
		
		List<String> conditionalExprNames = new ArrayList<>();
		VoidVisitor<List<String>> conditionalExprNameVisitor = new ConditionalExprCollector();
		conditionalExprNameVisitor.visit(cu, conditionalExprNames);
		conditionalExprNames.forEach(n -> System.out.println("Conditional Expression Collected: " + n));
		System.out.println("Conditional Expression Count: " + conditionalExprNames.size());
		writer.write(statementWriter(conditionalExprNames, "Conditional Expression" ));
		
		List<String> constructorDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> constructorDeclarationNameVisitor = new ConstructorDeclarationCollector();
		constructorDeclarationNameVisitor.visit(cu, constructorDeclarationNames);
		constructorDeclarationNames.forEach(n -> System.out.println("Constructor Declaration Collected: " + n));
		System.out.println("Constructor Declaration Count: " + constructorDeclarationNames.size());
		writer.write(statementWriter(constructorDeclarationNames, "Constructor Declaration" ));
		
		
		List<String> continueStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> continueStmtNameVisitor = new ContinueStmtCollector();
		continueStmtNameVisitor.visit(cu, continueStmtNames);
		continueStmtNames.forEach(n -> System.out.println("Continue Statement Collected: " + n));
		System.out.println("Continue Statement Count: " + continueStmtNames.size());
		writer.write(statementWriter(continueStmtNames, "Continue Statement" ));
		
		List<String> doStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> doStmtNameVisitor = new DoStmtCollector();
		doStmtNameVisitor.visit(cu, doStmtNames);
		doStmtNames.forEach(n -> System.out.println("Do Statement Collected: " + n));
		System.out.println("Do Statement Count: " + doStmtNames.size());
		writer.write(statementWriter(doStmtNames, "Do Statement" ));
		
		List<String> doubleLitExprNames = new ArrayList<>();
		VoidVisitor<List<String>> doubleLitExpVisitor = new DoubleLiteralExprCollector();
		doubleLitExpVisitor.visit(cu, doubleLitExprNames);
		doubleLitExprNames.forEach(n -> System.out.println("Double Literal Expression Collected: " + n));
		System.out.println("Double Literal Expression Count: " + doubleLitExprNames.size());
		writer.write(statementWriter(doStmtNames, "Double Literal Expression" ));
		
		List<String> emptyStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> emptyStmtVisitor = new EmptyStmtCollector();
		emptyStmtVisitor.visit(cu, emptyStmtNames);
		emptyStmtNames.forEach(n -> System.out.println("Empty Statement Collected: " + n));
		System.out.println("Empty Statement Count: " + emptyStmtNames.size());
		writer.write(statementWriter(emptyStmtNames, "Empty Statement" ));
		
		List<String> enclosedExprNames = new ArrayList<>();
		VoidVisitor<List<String>> enclosedExprVisitor = new EnclosedExprCollector();
		enclosedExprVisitor.visit(cu, enclosedExprNames);
		enclosedExprNames.forEach(n -> System.out.println("Enclosed Expression Collected: " + n));
		System.out.println("Enclosed Expression Count: " + enclosedExprNames.size());
		writer.write(statementWriter(enclosedExprNames, "Enclosed Expression" ));
		
		List<String> enumConstantDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> enumConstantDeclarationVisitor = new EnumConstantDeclarationCollector();
		enumConstantDeclarationVisitor.visit(cu, enumConstantDeclarationNames);
		enumConstantDeclarationNames.forEach(n -> System.out.println("Enum Constant Declaration Collected: " + n));
		System.out.println("Enum Constant Declaration Count: " + enumConstantDeclarationNames.size());
		writer.write(statementWriter(enumConstantDeclarationNames, "Enum Constant Declaration" ));
		
		
		List<String> enumDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> enumDeclarationVisitor = new EnumDeclarationCollector();
		enumDeclarationVisitor.visit(cu, enumDeclarationNames);
		enumDeclarationNames.forEach(n -> System.out.println("EnumDeclaration Collected: " + n));
		System.out.println("Enum Declaration Count: " + enumDeclarationNames.size());		
		writer.write(statementWriter(enumDeclarationNames, "Enum Declaration" ));
		
		List<String> explicitConstructorInvocationStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> explicitConstructorInvocationStmtVisitor = new ExplicitConstructorInvocationStmtCollector();
		explicitConstructorInvocationStmtVisitor.visit(cu, explicitConstructorInvocationStmtNames);
		explicitConstructorInvocationStmtNames.forEach(n -> System.out.println("Explicit Constructor Invocation Statment Collected: " + n));
		System.out.println("Explicit Constructor Invocation Statment Count: " + explicitConstructorInvocationStmtNames.size());	
		writer.write(statementWriter(explicitConstructorInvocationStmtNames, "Explicit Constructor Invocation Statment" ));
		
		List<String> expressionStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> expressionStmtVisitor = new ExpressionStmtCollector();
		expressionStmtVisitor.visit(cu, expressionStmtNames);
		expressionStmtNames.forEach(n -> System.out.println("Expression Statement Collected: " + n));
		System.out.println("Expression Statement Count: " + expressionStmtNames.size());		
		writer.write(statementWriter(expressionStmtNames, "Expression Statement" ));
		
		List<String> fieldAccessExprNames = new ArrayList<>();
		VoidVisitor<List<String>> fieldAccessExprVisitor = new FieldAccessExprCollector();
		fieldAccessExprVisitor.visit(cu, fieldAccessExprNames);
		fieldAccessExprNames.forEach(n -> System.out.println("Field Access Expression Collected: " + n));
		System.out.println("Field Access Expression Count: " + fieldAccessExprNames.size());		
		writer.write(statementWriter(fieldAccessExprNames, "Field Access Expression" ));
		
		List<String> fieldDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> fieldDeclarationVisitor = new FieldDeclarationCollector();
		fieldDeclarationVisitor.visit(cu, fieldDeclarationNames);
		fieldDeclarationNames.forEach(n -> System.out.println("Field Declaration Collected: " + n));
		System.out.println("Field Declaration Count: " + fieldDeclarationNames.size());
		writer.write(statementWriter(fieldDeclarationNames, "Field Declaration" ));
		
		List<String> foreachStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> foreachStmtVisitor = new ForeachStmtCollector();
		foreachStmtVisitor.visit(cu, foreachStmtNames);
		foreachStmtNames.forEach(n -> System.out.println("For Each Statement Collected: " + n));
		System.out.println("For Each Statement Count: " + foreachStmtNames.size());
		writer.write(statementWriter(foreachStmtNames, "For Each Statement" ));
		
		List<String> forStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> forStmtVisitor = new ForStmtCollector();
		forStmtVisitor.visit(cu, forStmtNames);
		forStmtNames.forEach(n -> System.out.println("For Statement Collected: " + n));
		System.out.println("For Statement Count: " + forStmtNames.size());
		writer.write(statementWriter(forStmtNames, "For Statement" ));
		
		List<String> ifStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> ifStmtVisitor = new IfStmtCollector();
		ifStmtVisitor.visit(cu, ifStmtNames);
		ifStmtNames.forEach(n -> System.out.println("If Statement Collected: " + n));
		System.out.println("If Statement Count: " + ifStmtNames.size());
		writer.write(statementWriter(ifStmtNames, "If Statement" ));
		
		List<String> importDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> importDeclarationVisitor = new ImportDeclarationCollector();
		importDeclarationVisitor.visit(cu, importDeclarationNames);
		importDeclarationNames.forEach(n -> System.out.println("Import Declaration Collected: " + n));
		System.out.println("Import Declaration Count: " + importDeclarationNames.size());
		writer.write(statementWriter(importDeclarationNames, "Import Declaration" ));
		
		
		
		List<String> initializerDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> initializerDeclarationVisitor = new InitializerDeclarationCollector();
		initializerDeclarationVisitor.visit(cu, initializerDeclarationNames);
		initializerDeclarationNames.forEach(n -> System.out.println("Initializer Declaration Collected: " + n));
		System.out.println("Initializer Declaration Count: " + initializerDeclarationNames.size());
		writer.write(statementWriter(initializerDeclarationNames, "Initializer Declaration" ));
		
		List<String> instanceOfExprNames = new ArrayList<>();
		VoidVisitor<List<String>> instanceOfExprVisitor = new InstanceOfExprCollector();
		instanceOfExprVisitor.visit(cu, instanceOfExprNames);
		instanceOfExprNames.forEach(n -> System.out.println("Instance Of Expression Collected: " + n));
		System.out.println("Instance Of Expression Count: " + instanceOfExprNames.size());
		writer.write(statementWriter(instanceOfExprNames, "Instance Of Expression" ));
	
		List<String> integerLiteralExprNames = new ArrayList<>();
		IntegerLiteralExprCollector integerLiteralExprVisitor = new IntegerLiteralExprCollector();
		integerLiteralExprVisitor.visit(cu, integerLiteralExprNames);
		integerLiteralExprNames.forEach(n -> System.out.println("Integer Literal Expression Collected: " + n));
		System.out.println("Integer Literal Expression Count: " + integerLiteralExprNames.size());
		writer.write(statementWriter(integerLiteralExprNames, "Integer Literal Expression" ));
	//	bw.write("leaf nodes: " + integerLiteralExprVisitor.getLeafNodes().toString() +  " \n size :" + 
	//	integerLiteralExprVisitor.getLeafNodes().size() + "\n" + integerLiteralExprVisitor.getParentNodes()+ "\n");
		leafMap.put("Integer Literal Expression", integerLiteralExprVisitor.getLeafNodes().size());
		
		
		
		List<String> intersectionTypeExprNames = new ArrayList<>();
		VoidVisitor<List<String>> intersectionTypeExprVisitor = new IntersectionTypeCollector();
		intersectionTypeExprVisitor.visit(cu, intersectionTypeExprNames);
		intersectionTypeExprNames.forEach(n -> System.out.println("Intersection Type Expression Collected: " + n));
		System.out.println("Intersection Type Expression Count: " + intersectionTypeExprNames.size() );
		writer.write(statementWriter(intersectionTypeExprNames, "Intersection Type Expression" ));
		
		
		List<String> javadocCommentNames = new ArrayList<>();
		VoidVisitor<List<String>> javadocCommentVisitor = new JavadocCommentCollector();
		javadocCommentVisitor.visit(cu, javadocCommentNames);
		javadocCommentNames.forEach(n -> System.out.println("Javadoc Comment Collected: " + n));
		System.out.println("Javadoc Comment Count: " + javadocCommentNames.size());
		writer.write(statementWriter(javadocCommentNames, "Javadoc Comment" ));
		
		List<String> labeledStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> labeledStmtVisitor = new LabeledStmtCollector();
		labeledStmtVisitor.visit(cu, labeledStmtNames);
		labeledStmtNames.forEach(n -> System.out.println("Labeled Statmen\n" + 
				"Void Type Count: 1ts Collected: " + n));
		System.out.println("Labeled Statment Count: " + labeledStmtNames.size());
		writer.write(statementWriter(labeledStmtNames, "Labeled Statment" ));
		
		List<String> lambdaExprNames = new ArrayList<>();
		VoidVisitor<List<String>> lambdaExprVisitor = new LambdaExprCollector();
		lambdaExprVisitor.visit(cu, lambdaExprNames);
		lambdaExprNames.forEach(n -> System.out.println("Lambda Expression Collected: " + n));
		System.out.println("Lambda Expression Count: " + lambdaExprNames.size());
		writer.write(statementWriter(lambdaExprNames, "Lambda Expression" ));
		
		List<String> lineCommentNames = new ArrayList<>();
		VoidVisitor<List<String>> lineCommentVisitor = new LineCommentCollector();
		lineCommentVisitor.visit(cu, lineCommentNames);
		lineCommentNames.forEach(n -> System.out.println("Line Comment Collected: " + n));
		System.out.println("Line Comment Count: " + lineCommentNames.size());
		writer.write(statementWriter(lineCommentNames, "Line Comment" ));
		
		List<String> localClassDeclarationStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> localClassDeclarationStmtVisitor = new LocalClassDeclarationStmtCollector();
		localClassDeclarationStmtVisitor.visit(cu, localClassDeclarationStmtNames);
		localClassDeclarationStmtNames.forEach(n -> System.out.println("Local Class Declaration Stmt Collected: " + n));
		System.out.println("Local Class Declaration Stmt Count: " + localClassDeclarationStmtNames.size());
		writer.write(statementWriter(localClassDeclarationStmtNames, "Local Class Declaration Stmt" ));
		
		List<String> longLiteralExprNames = new ArrayList<>();
		VoidVisitor<List<String>> longLiteralExprVisitor = new LongLiteralExprCollector();
		longLiteralExprVisitor.visit(cu, longLiteralExprNames);
		longLiteralExprNames.forEach(n -> System.out.println("Long Literal Expression Collected: " + n));
		System.out.println("Long Literal Expression Count: " + longLiteralExprNames.size());
		writer.write(statementWriter(longLiteralExprNames, "Long Literal Expression" ));
		
		List<String> markerAnnotationExprNames = new ArrayList<>();
		VoidVisitor<List<String>> markerAnnotationExprVisitor = new MarkerAnnotationExprCollector();
		markerAnnotationExprVisitor.visit(cu, markerAnnotationExprNames);
		markerAnnotationExprNames.forEach(n -> System.out.println("Marker Annotation Expression Collected: " + n));
		System.out.println("Marker Annotation Expression Count: " + markerAnnotationExprNames.size());
		writer.write(statementWriter(markerAnnotationExprNames, "Marker Annotation Expression" ));
		
		List<String> memberValuePairNames = new ArrayList<>();
		VoidVisitor<List<String>> memberValuePairVisitor = new MemberValuePairCollector();
		memberValuePairVisitor.visit(cu, memberValuePairNames);
		memberValuePairNames.forEach(n -> System.out.println("Member Value Pair Collected: " + n));
		System.out.println("Member Value Pair Count: " + memberValuePairNames.size());
		writer.write(statementWriter(memberValuePairNames, "Member Value Pair" ));
		
		List<String> methodCallExprNames = new ArrayList<>();
		VoidVisitor<List<String>> methodCallExprVisitor = new MethodCallExprCollector();
		methodCallExprVisitor.visit(cu, methodCallExprNames);
		methodCallExprNames.forEach(n -> System.out.println("Method Call Expression Collected: " + n));
		System.out.println("Method Call Expression Count: " + methodCallExprNames.size());
		writer.write(statementWriter(methodCallExprNames, "Method Call Expression" ));
		
		List<String> methodNames = new ArrayList<>();
		MethodNameCollector methodNamesCollector = new MethodNameCollector();
		methodNamesCollector.visit(cu, methodNames);
		methodNames.forEach(n -> System.out.println("Method Collected: " + n));
		System.out.println("Method Count: " + methodNames.size());
		writer.write(statementWriter(methodNames, "Method" ));
		
		List<String> methodReferenceExprNames = new ArrayList<>();
		VoidVisitor<List<String>> methodReferenceExprVisitor = new MethodReferenceExprCollector();
		methodReferenceExprVisitor.visit(cu, methodReferenceExprNames);
		methodReferenceExprNames.forEach(n -> System.out.println("Method Reference Expression Collected: " + n));
		System.out.println("Method Reference Expression Count: " + methodReferenceExprNames.size());
		writer.write(statementWriter(methodReferenceExprNames, "Method Reference Expression" ));
		
		List<String> nameNames = new ArrayList<>();
		VoidVisitor<List<String>> nameVisitor = new NameCollector();
		nameVisitor.visit(cu, nameNames);
		nameNames.forEach(n -> System.out.println("Name Collected: " + n));
		System.out.println("Name Count: " + nameNames.size());
		writer.write(statementWriter(nameNames, "Name" ));
		
		List<String> nameExprNames = new ArrayList<>();
		VoidVisitor<List<String>> nameExprVisitor = new NameExprCollector();
		nameExprVisitor.visit(cu, nameExprNames);
		nameExprNames.forEach(n -> System.out.println("Name Expression Collected: " + n));
		System.out.println("Name Expression Count: " + nameExprNames.size());
		writer.write(statementWriter(nameExprNames, "Name Expression" ));
		
		List<String> nodeListNames = new ArrayList<>();
		VoidVisitor<List<String>> nodeListVisitor = new NodeListCollector();
		nodeListVisitor.visit(cu, nodeListNames);
		nodeListNames.forEach(n -> System.out.println("Node List Collected: " + n));
		System.out.println("Node List Count: " + nodeListNames.size());
		writer.write(statementWriter(nodeListNames, "Node List" ));
		
		List<String> normalAnnotationExprNames = new ArrayList<>();
		VoidVisitor<List<String>> normalAnnotationExprVisitor = new NormalAnnotationExprCollector();
		normalAnnotationExprVisitor.visit(cu, normalAnnotationExprNames);
		normalAnnotationExprNames.forEach(n -> System.out.println("Normal Annotation Expression Collected: " + n));
		System.out.println("Normal Annotation Expression Count: " + normalAnnotationExprNames.size());
		writer.write(statementWriter(normalAnnotationExprNames, "Normal Annotation Expression" ));
		
		List<String> nullLiteralExprNames = new ArrayList<>();
		VoidVisitor<List<String>> nullLiteralExprVisitor = new NullLiteralExprCollector();
		nullLiteralExprVisitor.visit(cu, nullLiteralExprNames);
		nullLiteralExprNames.forEach(n -> System.out.println("Null Literal Expression Collected: " + n));
		System.out.println("Null Literal Expression Count: " + nullLiteralExprNames.size());
		writer.write(statementWriter(nullLiteralExprNames, "Null Literal Expression" ));
		
		List<String> objectCreationExprNames = new ArrayList<>();
		VoidVisitor<List<String>> objectCreationExprVisitor = new ObjectCreationExprCollector();
		objectCreationExprVisitor.visit(cu, objectCreationExprNames);
		objectCreationExprNames.forEach(n -> System.out.println("Object Creation Expression Collected: " + n));
		System.out.println("Object Creation Expression Count: " + objectCreationExprNames.size());
		writer.write(statementWriter(objectCreationExprNames, "Object Creation Expression" ));
		
		List<String> packageDeclarationNames = new ArrayList<>();
		VoidVisitor<List<String>> packageDeclarationVisitor = new PackageDeclarationCollector();
		packageDeclarationVisitor.visit(cu, packageDeclarationNames);
		packageDeclarationNames.forEach(n -> System.out.println("Package Declaration Collected: " + n));
		System.out.println("Package Declaration Count: " + packageDeclarationNames.size());
		writer.write(statementWriter(packageDeclarationNames, "Package Declaration" ));
		
		List<String> parameterNames = new ArrayList<>();
		VoidVisitor<List<String>> parameterVisitor = new ParameterCollector();
		parameterVisitor.visit(cu, parameterNames);
		parameterNames.forEach(n -> System.out.println("Parameter Collected: " + n));
		System.out.println("Parameter Count: " + parameterNames.size());
		writer.write(statementWriter(parameterNames, "Parameter" ));
		
		List<String> primitiveTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> primitiveTypeVisitor = new PrimitiveTypeCollector();
		primitiveTypeVisitor.visit(cu, primitiveTypeNames);
		primitiveTypeNames.forEach(n -> System.out.println("Primitive Type Collected: " + n));
		System.out.println("Primitive Type Count: " + primitiveTypeNames.size());
		writer.write(statementWriter(primitiveTypeNames, "Primitive Type" ));
		
		List<String> simpleNameNames = new ArrayList<>();
		SimpleNameCollector simpleNameVisitor = new SimpleNameCollector();
		simpleNameVisitor.visit(cu, simpleNameNames);
		simpleNameNames.forEach(n -> System.out.println("Simple Name Collected: " + n));
//		bw.write("leaf nodes: " + simpleNameVisitor.getLeafNodes().toString() +  " \n size :" + 
		//		simpleNameVisitor.getLeafNodes().size() + "\n" + simpleNameVisitor.getParentNodes()+ "\n");
		leafMap.put("Simple Name", simpleNameVisitor.getLeafNodes().size());
		
		
			
			
			
		
	
		
		System.out.println("Simple Name Count: " + simpleNameNames.size());
		writer.write(statementWriter(simpleNameNames, "Simple Name" ));
		
		List<String> singleMemberAnnotationExprNames = new ArrayList<>();
		VoidVisitor<List<String>> singleMemberAnnotationExprVisitor = new SingleMemberAnnotationExprCollector();
		singleMemberAnnotationExprVisitor.visit(cu, singleMemberAnnotationExprNames);
		singleMemberAnnotationExprNames.forEach(n -> System.out.println("Single Member Annotation Expression Collected: " + n));
		System.out.println("Single Member Annotation Expression Count: " + singleMemberAnnotationExprNames.size());
		writer.write(statementWriter(singleMemberAnnotationExprNames, "Single Member Annotation Expression" ));
		
		List<String> stringLiteralExprNames = new ArrayList<>();
		StringLiteralExprCollector stringLiteralExprVisitor = new StringLiteralExprCollector();
		stringLiteralExprVisitor.visit(cu, stringLiteralExprNames);
		stringLiteralExprNames.forEach(n -> System.out.println("String Literal Expression Collected: " + n));
		System.out.println("Single Literal Expression Count: " + stringLiteralExprNames.size());
		writer.write(statementWriter(stringLiteralExprNames, "Single Literal Expression" ));
		
	//	bw.write(stringLiteralExprVisitor.getLeafNodes().toString() + "\n");
		
		
		
		List<String> superExprNames = new ArrayList<>();
		VoidVisitor<List<String>> superExprVisitor = new SuperExprCollector();
		superExprVisitor.visit(cu, superExprNames);
		superExprNames.forEach(n -> System.out.println("Super Expression Collected: " + n));
		System.out.println("Super Expression Count: " + superExprNames.size());
		writer.write(statementWriter(superExprNames, "Super Expression" ));
		
		List<String> switchEntryStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> switchEntryStmtVisitor = new SwitchEntryStmtCollector();
		switchEntryStmtVisitor.visit(cu, switchEntryStmtNames);
		switchEntryStmtNames.forEach(n -> System.out.println("Switch Entry Statement Collected: " + n));
		System.out.println("Switch Entry Statement Count: " + switchEntryStmtNames.size());
		writer.write(statementWriter(switchEntryStmtNames, "Switch Entry Statement" ));
		
		List<String> switchStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> switchStmtVisitor = new SwitchStmtCollector();
		switchStmtVisitor.visit(cu, switchStmtNames);
		switchStmtNames.forEach(n -> System.out.println("Switch Statement Collected: " + n));
		System.out.println("Switch Statement Count: " + switchStmtNames.size());
		writer.write(statementWriter(switchStmtNames, "Switch Statement" ));
		
		List<String> synchronizedStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> synchronizedStmtVisitor = new SynchronizedStmtCollector();
		synchronizedStmtVisitor.visit(cu, synchronizedStmtNames);
		synchronizedStmtNames.forEach(n -> System.out.println("Synchronized Statement Collected: " + n));
		System.out.println("Synchronized Statement Count: " + synchronizedStmtNames.size());
		writer.write(statementWriter(synchronizedStmtNames, "Synchronized Statement" ));
		
		List<String> thisExprNames = new ArrayList<>();
		VoidVisitor<List<String>> thisExprVisitor = new ThisExprCollector();
		thisExprVisitor.visit(cu, thisExprNames);
		thisExprNames.forEach(n -> System.out.println("This Expression Collected: " + n));
		System.out.println("This Expression Count: " + thisExprNames.size());
		writer.write(statementWriter(thisExprNames, "This Expression" ));
		
		List<String> throwStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> throwStmtVisitor = new ThrowStmtCollector();
		throwStmtVisitor.visit(cu, throwStmtNames);
		throwStmtNames.forEach(n -> System.out.println("Throw Statement Collected: " + n));
		System.out.println("Throw Statement Count: " + throwStmtNames.size());
		writer.write(statementWriter(throwStmtNames, "Throw Statement" ));
		
		List<String> tryStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> tryStmtVisitor = new TryStmtCollector();
		tryStmtVisitor.visit(cu, tryStmtNames);
		tryStmtNames.forEach(n -> System.out.println("Try Statement Collected: " + n));
		System.out.println("Try Statement Count: " + tryStmtNames.size());
		writer.write(statementWriter(tryStmtNames, "Try Statement" ));
		
		List<String> typeExprNames = new ArrayList<>();
		VoidVisitor<List<String>> typeExprVisitor = new TypeExprCollector();
		typeExprVisitor.visit(cu, typeExprNames);
		typeExprNames.forEach(n -> System.out.println("Type Expression Collected: " + n));
		System.out.println("Type Expression Count: " + typeExprNames.size());
		writer.write(statementWriter(typeExprNames, "Type Expression" ));
		
		List<String> typeParameterNames = new ArrayList<>();
		VoidVisitor<List<String>> typeParameterVisitor = new TypeParameterCollector();
		typeParameterVisitor.visit(cu, typeParameterNames);
		typeParameterNames.forEach(n -> System.out.println("Type Parameter Collected: " + n));
		System.out.println("Type Parameter Count: " + typeParameterNames.size());
		writer.write(statementWriter(typeParameterNames, "Type Parameter" ));
		
		List<String> unaryExprNames = new ArrayList<>();
		VoidVisitor<List<String>> unaryExprVisitor = new UnaryExprCollector();
		unaryExprVisitor.visit(cu, unaryExprNames);
		unaryExprNames.forEach(n -> System.out.println("Unary Expression Collected: " + n));
		System.out.println("Unary Expression Count: " + unaryExprNames.size());
		writer.write(statementWriter(unaryExprNames, "Unary Expression" ));
		
		List<String> unionTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> unionTypeVisitor = new UnionTypeCollector();
		unionTypeVisitor.visit(cu, unionTypeNames);
		unionTypeNames.forEach(n -> System.out.println("Union Type Collected: " + n));
		System.out.println("Union Type Count: " + unionTypeNames.size());
		writer.write(statementWriter(unionTypeNames, "Union Type" ));
		
		List<String> unknownTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> unknownTypeVisitor = new UnknownTypeCollector();
		unknownTypeVisitor.visit(cu, unknownTypeNames);
		unknownTypeNames.forEach(n -> System.out.println("Unknown Type Collected: " + n));
		System.out.println("Unknown Type Count: " + unknownTypeNames.size());
		writer.write(statementWriter(unknownTypeNames, "Unknown Type" ));
		
		List<String> varDecExprNames = new ArrayList<>();
		VoidVisitor<List<String>> varDecExprVisitor = new VariableDeclarationExprCollector();
		varDecExprVisitor.visit(cu, varDecExprNames);
		varDecExprNames.forEach(n -> System.out.println("Variable Declaration Expression Collected: " + n));
		System.out.println("Variable Declaration Expression Count: " + varDecExprNames.size());
		writer.write(statementWriter(varDecExprNames, "Variable Declaration Expression" ));
		
		List<String> varDecNames = new ArrayList<>();
		VoidVisitor<List<String>> varDecVisitor = new VariableDeclaratorCollector();
		varDecVisitor.visit(cu, varDecExprNames);
		varDecNames.forEach(n -> System.out.println("Variable Declarator Collected: " + n));
		System.out.println("Variable Declarator Count: " + varDecNames.size());
		writer.write(statementWriter(varDecNames, "Variable Declarator" ));
		
		List<String> voidTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> voidTypeVisitor = new VoidTypeCollector();
		voidTypeVisitor.visit(cu, voidTypeNames);
		voidTypeNames.forEach(n -> System.out.println("Void Type Collected: " + n));
		System.out.println("Void Type Count: " + voidTypeNames.size());
		writer.write(statementWriter(voidTypeNames, "Void Type" ));
		
		List<String> whileStmtNames = new ArrayList<>();
		VoidVisitor<List<String>> whileStmtVisitor = new WhileStmtCollector();
		whileStmtVisitor.visit(cu, whileStmtNames);
		whileStmtNames.forEach(n -> System.out.println("While Statment Collected: " + n));
		System.out.println("While Statement Count: " + whileStmtNames.size());
		writer.write(statementWriter(whileStmtNames, "While Statement" ));
		
		List<String> wildcardTypeNames = new ArrayList<>();
		VoidVisitor<List<String>> wildcardTypeVisitor = new WildcardTypeCollector();
		wildcardTypeVisitor.visit(cu, wildcardTypeNames);
		wildcardTypeNames.forEach(n -> System.out.println("Wild Card Type Collected: " + n));
		System.out.println("Wild Card Type Count: " + wildcardTypeNames.size());
		writer.write(statementWriter(wildcardTypeNames, "Wild Card Type" ));
		
		//iterate through leafMap, to find total number of leaf nodes 
		
		double leafCount = 0.00;  
		double nodeTypeCount = 0.00;  
		
		for (Integer value : leafMap.values()) {
		    
			leafCount += value; 
		}
		
		//finding leaf node frequency by finding number of a particular type of node, divided by total number of nodes 
		//try to find for particular instance? 
	/*	for (String key : leafMap.keySet()) {
		    
			 
			bw.write(key + " Node frequency : " + leafMap.get(key)/leafCount + "\n");
		}
		
	*/	
	//	bw.write( "\n Total leaf nodes : " + leafCount);
		writer.close();
		writer1.close();
	//	bw.close();
		fwriter.close();
		fwriter1.close();
	}
			}
				 }
		
	catch(IOException x) {
		 System.err.println(x);
	}
	
	 
	
	
	}
	
}

