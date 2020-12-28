	.data
data:	.word 8, 5, 14, 10, 12, 3, 9, 6, 1, 15, 7, 4, 13, 2, 11
size:	.word 15
#use below sample if above example is too large to debug
# data:	.word 4, 2, 5, 3, 1
# size:	.word 5
	.text

partition:
	# TODO: fill in your code here
	addi $sp, $sp, -16
	sw $ra, 12($sp)
	sw $a0, 8($sp)
	sw $a1, 4($sp)
	sw $a2, 0($sp)
	move $s1, $a1 # s1 is left
	move $s2, $a2 # s2 is right
	sll $t0, $s1, 2 
	sll $t1, $s2, 2 
	add $t2, $a0, $t0  # t2 is for ref
	lw $t3, ($t2)   	# t3 is pivot
	slt $t4, $s1, $s2
	bne $t4, $zero, L1

L1:
	addu $t2, $a0, $t1   
	lw $t4, ($t2) 		# t4 is data[right]
	slt $t2, $s1, $s2
	beq $t2, $zero, last
	slt $t2, $t3, $t4	
	bne $t2, $zero, L2
	slt $t2, $s1, $s2
	j test2
L2:
	addi $s2, $s2, -1
	sll $t1, $s2, 2 
	addu $t2, $a0, $t1
	lw $t4, ($t2)
	slt $t2, $t3, $t4
	bne $t2, $zero, L2
	j test2

L3:
	addi $s1, $s1, 1
	sll $t0, $s1, 2 
	j test2

last:
	sll $t7, $a1, 2
	add $t8, $a0, $t7   
	lw $s3, 0($t8)      
	add $t2, $a0, $t1   
	lw $s4, 0($t2)      
	sw $s3, 0($t2)
	sll $t9, $a1, 2
	add $t9, $a0, $t9      
	sw $s4, 0($t9)
	add $v0, $s2, $zero
	lw $a0, 8($sp)
	lw $a1, 4($sp)
	lw $a2, 0($sp)
	lw $ra, 12($sp)
	addi $sp, $sp, 16
	jr $ra

test2:
	slt $t2, $s1, $s2
	beq $t2, $zero, test3
	addu $t2, $a0, $t0
	lw $t5, ($t2)
	slt $t6, $t5, $t3
	bne $t6, $zero, L3
	beq $t5, $t3, L3
	j test3

test3:
	slt $t4, $s1, $s2
	bne $t4, $zero, swap

swap:
	add $t8, $a0, $t1   
	lw $s3, 0($t8)      
	add $t2, $a0, $t0   
	lw $s4, 0($t2)      
	sw $s4, 0($t8)      
	sw $s3, 0($t2)
	slt $t4, $s1, $s2
	bne $t4, $zero, L1      
	j last


quick_sort:
# 	# TODO: fill in your code here
	addi $sp, $sp, -20
	sw  $ra, 16($sp)
	sw  $a0, 12($sp)  # data
	sw  $a1, 8($sp)  # start
	sw  $s6, 4($sp)  # end
	sw  $s0, 0($sp)
	slt $t0, $a1, $a2
	beq $t0, $zero, return
	move $s6, $a2
	jal partition
	move $s0, $v0
	addi $a2, $s0, -1
	jal quick_sort
	addi $a1, $s0, 1
	move $a2, $s6
	# add  $a2, $t1, $zero
	jal quick_sort		 

return:
	lw $a0, 12($sp)			
 	lw $a1, 8($sp)			
 	lw $s6, 4($sp)
	lw $s0, 0($sp)			
 	lw $ra, 16($sp)			
 	addi $sp, $sp, 20		
 	jr $ra
	


main:
	la 	$a0, data				#load address of "data"."la" is pseudo instruction, see Appendix A-66 of text book.
	addi 	$a1, $zero, 0
	lw 	$a2, size				#load data "size"
	addi	$a2, $a2, -1
	addi 	$sp, $sp, -4
	sw	$ra, 0($sp)
	jal 	quick_sort			#quick_sort(data,0,size-1)
	lw	$ra, 0($sp)
	addi	$sp, $sp, 4
	jr 	$ra
